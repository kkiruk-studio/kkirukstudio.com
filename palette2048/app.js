/* Palette landing — the hero board mirrors the day's real painting: each of the
   16 tiles takes the dominant color of that region of the artwork, snapped to
   the app's curated palette. A real painting fades in beside it. */
(function () {
  var PAINTINGS = [
    { img: "starry-night.jpg", name: "The Starry Night", artist: "Vincent van Gogh",
      c: ["#16377A","#4E8E79","#4E8E79","#4E8E79","#4E8E79","#4E8E79","#4E8E79","#2B6E9D","#151A19","#4E8E79","#4E8E79","#4E8E79","#151A19","#151A19","#16377A","#16377A"] },
    { img: "sunflowers.jpg", name: "Sunflowers", artist: "Vincent van Gogh",
      c: ["#DEBA58","#DEBA58","#DEBA58","#C78F36","#7C2E1C","#C78F36","#C78F36","#C78F36","#197C6F","#C78F36","#C78F36","#197C6F","#C78F36","#C78F36","#C78F36","#C78F36"] },
    { img: "scream.jpg", name: "The Scream", artist: "Edvard Munch",
      c: ["#B3532A","#B3532A","#C0A365","#C0A365","#C0A365","#C0A365","#2D2623","#2D2623","#B3532A","#C0A365","#2D2623","#2D2623","#B3532A","#2D2623","#2D2623","#2D2623"] },
    { img: "kiss.jpg", name: "The Kiss", artist: "Gustav Klimt",
      c: ["#896D23","#896D23","#896D23","#896D23","#896D23","#D4B645","#D4B645","#896D23","#896D23","#D4B645","#D4B645","#896D23","#896D23","#896D23","#896D23","#896D23"] },
    { img: "mona-lisa.jpg", name: "Mona Lisa", artist: "Leonardo da Vinci",
      c: ["#95A146","#95A146","#95A146","#95A146","#8F5A24","#290E25","#290E25","#8F5A24","#290E25","#290E25","#290E25","#290E25","#190E2B","#290E25","#190E2B","#190E2B"] }
  ];

  var board = document.getElementById("board");
  if (!board) return;
  var cells = board.querySelectorAll("span");
  var nameEl = document.getElementById("paintName");
  var artistEl = document.getElementById("paintArtist");
  var imgEl = document.getElementById("paintImg");
  var i = 0;
  for (var pi = 0; pi < PAINTINGS.length; pi++) { var pre = new Image(); pre.src = "assets/paintings/" + PAINTINGS[pi].img; }

  function paint(p) {
    for (var k = 0; k < cells.length; k++) {
      cells[k].style.backgroundColor = p.c[k % p.c.length];
    }
    if (imgEl && p.img) {
      imgEl.style.opacity = 0;
      setTimeout(function () { imgEl.src = "assets/paintings/" + p.img; imgEl.style.opacity = 1; }, 520);
    }
    if (nameEl) nameEl.textContent = p.name;
    if (artistEl) artistEl.textContent = p.artist;
  }

  paint(PAINTINGS[0]);
  setInterval(function () {
    i = (i + 1) % PAINTINGS.length;
    paint(PAINTINGS[i]);
  }, 3200);
})();
