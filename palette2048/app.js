/* Palette landing — the hero board cycles through real painting palettes,
   the way the app paints a new masterpiece each day. */
(function () {
  var PAINTINGS = [
    { name: "The Starry Night", artist: "Vincent van Gogh",
      c: ["#151A19","#16377A","#1E4E63","#2B6E9D","#4E8E79","#7C9A5A","#B49A2D","#C9B84A","#D8D391"] },
    { name: "Sunflowers", artist: "Vincent van Gogh",
      c: ["#2A3915","#4A4018","#7C2E1C","#197C6F","#8A6A2E","#C78F36","#D0A23A","#D8B14A","#DEBA58"] },
    { name: "The Scream", artist: "Edvard Munch",
      c: ["#1F2E3A","#2E3E4E","#3A4A5A","#7A5436","#B5642A","#C97A30","#D98A3A","#E0A94E","#EFD89A"] },
    { name: "The Kiss", artist: "Gustav Klimt",
      c: ["#2A2410","#4A3E14","#6E5A1E","#94781E","#B8941E","#CDA838","#D9B94A","#E8D27A","#F2E6B0"] },
    { name: "Mona Lisa", artist: "Leonardo da Vinci",
      c: ["#1A140C","#2A2012","#3B2E1A","#54462A","#6B5A38","#857046","#9A8456","#C0A878","#E0D2A8"] }
  ];

  var board = document.getElementById("board");
  if (!board) return;
  var cells = board.querySelectorAll("span");
  var nameEl = document.getElementById("paintName");
  var artistEl = document.getElementById("paintArtist");
  var i = 0;

  function paint(p) {
    for (var k = 0; k < cells.length; k++) {
      cells[k].style.backgroundColor = p.c[Math.floor(k * p.c.length / cells.length)];
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
