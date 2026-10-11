// Local Link place pages — geocoding cache builder (MapKit MKLocalSearch, no API key).
//
// Usage (from repo root):
//   python3 locallink/places_build.py --geo-input /tmp/places_geo_input.json
//   swiftc -O -parse-as-library locallink/places_geocode.swift -o /tmp/places_geocode
//   /tmp/places_geocode /tmp/places_geo_input.json locallink/places_geo.json [--retry]
//
// Input: [{slug, name, localName, cityLocal, cityEn, cityLat, cityLng, terms[], chain}]
// Output (places_geo.json, sorted keys): {slug: {status, lat?, lng?, result?, query?, reason?}}
//   status = "ok" | "rejected" (a result came back but failed validation) | "notfound"
// Slugs already present in the cache are skipped unless --retry (re-tries non-"ok" only).
//
// Validation (a wrong pin is worse than no pin):
//   1. result name must loosely match a known spelling (localName, name, its " · " parts, alias
//      variants): case/space/punctuation-insensitive substring in either direction, with the
//      shorter string covering at least 75% of the longer one.
//   2. result must not be a city/province/country-level area (e.g. "서울특별시", "Tokyo"):
//      rejected when its name equals the placemark's locality / administrativeArea /
//      country, or equals the city name (+ an administrative suffix).
//   3. result must be within 120 km of the app's city centre.
//   4. no pin for chains: alias tagged generated-chain, or 2+ same-named, same-category hits >0.5 km apart.
//   5. a bare road (no POI category, name == thoroughfare) only counts on an exact name match.
// Queries tried in order until one passes: "<localName> <local city>" and "<name> <English city>"
// as POI-only searches, then bare "<localName>" (region-biased POI search). Address-type results
// were dropped after a trial run: they only ever returned districts, roads or the city itself. Result names come back in the system language, so all alias
// spellings (incl. Korean) are used as match terms. Hits are ranked exact-name first.
// 0.3 s between requests; MapKit throttling backs off 30 s and retries.

import Foundation
import MapKit

struct InputPlace: Decodable {
    let slug: String
    let name: String
    let localName: String
    let cityLocal: String
    let cityEn: String
    let cityLat: Double
    let cityLng: Double
    let terms: [String]
    let chain: Bool
}

func norm(_ s: String) -> String {
    s.lowercased()
        .folding(options: [.diacriticInsensitive, .widthInsensitive], locale: nil)
        .components(separatedBy: CharacterSet.alphanumerics.inverted).joined()
}

let adminSuffixes = ["특별시", "광역시", "특별자치시", "특별자치도", "시", "도", "市", "都", "府", "県", "省",
                     "city", "metropolitancity", "prefecture", "province", "specialadministrativeregion", "sar"]

func isAdminArea(_ item: MKMapItem, place: InputPlace) -> Bool {
    let n = norm(item.name ?? "")
    if n.isEmpty { return true }
    let pm = item.placemark
    for a in [pm.locality, pm.administrativeArea, pm.country, pm.subAdministrativeArea == pm.locality ? pm.subAdministrativeArea : nil] {
        if let a = a, norm(a) == n { return true }
    }
    for city in [place.cityLocal, place.cityEn] {
        let c = norm(city)
        if c.isEmpty { continue }
        if n == c { return true }
        for suf in adminSuffixes where n == c + norm(suf) { return true }
    }
    return false
}

func looselyMatches(_ result: String, terms: [String]) -> Bool {
    let r = norm(result)
    if r.isEmpty { return false }
    for t in terms {
        let q = norm(t)
        if q.isEmpty { continue }
        // Containment either way, but the shorter must cover >= 60% of the longer:
        // "명동" must not satisfy "명동교자", and "보코 서울 명동" (a hotel) / "성수옥" must not satisfy "명동" / "성수".
        if (r.contains(q) || q.contains(r)) && min(r.count, q.count) >= 2 &&
            Double(min(r.count, q.count)) >= Double(max(r.count, q.count)) * 0.75 { return true }
    }
    return false
}

func distanceKm(_ a: CLLocationCoordinate2D, _ lat: Double, _ lng: Double) -> Double {
    CLLocation(latitude: a.latitude, longitude: a.longitude)
        .distance(from: CLLocation(latitude: lat, longitude: lng)) / 1000
}

func search(_ query: String, near p: InputPlace, types: MKLocalSearch.ResultType) async -> (items: [MKMapItem], throttled: Bool) {
    let req = MKLocalSearch.Request()
    req.naturalLanguageQuery = query
    req.region = MKCoordinateRegion(center: CLLocationCoordinate2D(latitude: p.cityLat, longitude: p.cityLng),
                                    span: MKCoordinateSpan(latitudeDelta: 0.6, longitudeDelta: 0.6))
    req.resultTypes = types
    do {
        let resp = try await MKLocalSearch(request: req).start()
        return (resp.mapItems, false)
    } catch let e as MKError where e.code == .loadingThrottled {
        return ([], true)
    } catch {
        return ([], false)
    }
}

func round6(_ v: Double) -> NSDecimalNumber { NSDecimalNumber(string: String(format: "%.6f", v)) }

@main
struct Geocode {
    static func main() async {
        setvbuf(stdout, nil, _IOLBF, 0)
        let args = CommandLine.arguments
        guard args.count >= 3 else {
            FileHandle.standardError.write("usage: places_geocode <input.json> <places_geo.json> [--retry]\n".data(using: .utf8)!)
            exit(2)
        }
        let retry = args.contains("--retry")
        let inURL = URL(fileURLWithPath: args[1]), outURL = URL(fileURLWithPath: args[2])
        let places = try! JSONDecoder().decode([InputPlace].self, from: Data(contentsOf: inURL))
        var cache: [String: [String: Any]] = [:]
        if let d = try? Data(contentsOf: outURL),
           let obj = try? JSONSerialization.jsonObject(with: d) as? [String: [String: Any]] {
            cache = obj
        }
        func save() {
            let d = try! JSONSerialization.data(withJSONObject: cache, options: [.prettyPrinted, .sortedKeys, .withoutEscapingSlashes])
            try! (d + "\n".data(using: .utf8)!).write(to: outURL)
        }
        var done = 0
        for p in places {
            if let c = cache[p.slug], !(retry && (c["status"] as? String) != "ok") { continue }
            let terms = [p.localName, p.name] + p.name.components(separatedBy: " · ") + p.terms
            var entry: [String: Any] = ["status": "notfound"]
            var reasons: [String] = []
            let attempts: [(String, MKLocalSearch.ResultType)] = [
                ("\(p.localName) \(p.cityLocal)", .pointOfInterest),
                ("\(p.name) \(p.cityEn)", .pointOfInterest),
                (p.localName, .pointOfInterest),
            ]
            for (query, types) in attempts {
                var res = await search(query, near: p, types: types)
                var waits = 0
                while res.throttled && waits < 6 {
                    waits += 1
                    try? await Task.sleep(nanoseconds: 30_000_000_000)
                    res = await search(query, near: p, types: types)
                }
                try? await Task.sleep(nanoseconds: 300_000_000)
                if res.items.isEmpty { continue }
                var passing: [MKMapItem] = []
                for item in res.items.prefix(5) {
                    let n = item.name ?? ""
                    if isAdminArea(item, place: p) { reasons.append("admin-area:\(n)"); continue }
                    if !looselyMatches(n, terms: terms) { reasons.append("name-mismatch:\(n)"); continue }
                    let exact = terms.contains { norm($0) == norm(n) }
                    if item.pointOfInterestCategory == nil, let tf = item.placemark.thoroughfare,
                       norm(tf) == norm(n), !exact { reasons.append("road:\(n)"); continue }
                    let km = distanceKm(item.placemark.coordinate, p.cityLat, p.cityLng)
                    if km > 120 { reasons.append("too-far:\(n):\(Int(km))km"); continue }
                    passing.append(item)
                }
                // Several same-named hits far apart = branches of a chain; we cannot know which one
                // the traveller means, so no pin. Chain-tagged aliases are never pinned either.
                // Prefer a hit whose name is exactly one of the known spellings.
                passing.sort { a, b in
                    let ea = terms.contains { norm($0) == norm(a.name ?? "") }
                    let eb = terms.contains { norm($0) == norm(b.name ?? "") }
                    return ea && !eb
                }
                if let first = passing.first {
                    let branches = passing.dropFirst().filter {
                        norm($0.name ?? "") == norm(first.name ?? "") &&
                        $0.pointOfInterestCategory != nil && $0.pointOfInterestCategory == first.pointOfInterestCategory &&
                        distanceKm($0.placemark.coordinate, first.placemark.coordinate.latitude, first.placemark.coordinate.longitude) > 0.5
                    }
                    if p.chain || !branches.isEmpty {
                        entry = ["status": "rejected", "reason": "ambiguous-branches:\(first.name ?? "")"]
                        reasons = []
                        break
                    }
                }
                if let it = passing.first {
                    entry = ["status": "ok", "query": query, "result": it.name ?? "",
                             "lat": round6(it.placemark.coordinate.latitude),
                             "lng": round6(it.placemark.coordinate.longitude)]
                    break
                }
            }
            if (entry["status"] as? String) == "notfound" && !reasons.isEmpty {
                entry = ["status": "rejected", "reason": Array(reasons.prefix(4)).joined(separator: " | ")]
            }
            cache[p.slug] = entry
            done += 1
            print("\(p.slug)\t\(entry["status"]!)\t\(entry["result"] ?? entry["reason"] ?? "")")
            if done % 20 == 0 { save() }
        }
        save()
        let ok = cache.values.filter { ($0["status"] as? String) == "ok" }.count
        let rej = cache.values.filter { ($0["status"] as? String) == "rejected" }.count
        let nf = cache.values.filter { ($0["status"] as? String) == "notfound" }.count
        print("total \(cache.count) · ok \(ok) · rejected \(rej) · notfound \(nf)")
    }
}
