/* Palette landing — the hero board is a stylized 4x4 of the day's real painting:
   each tile takes a color from that region of the artwork (the app's curated
   palette), so the board reads as a mini masterpiece. The painting fades in beside it. */
(function () {
  var PAINTINGS = [
    { img: "starry-night.jpg", name: "The Starry Night", artist: "Vincent van Gogh",
      c: ["#16377A","#2B6E9D","#4E8E79","#D8D391","#2B6E9D","#16377A","#D8D391","#2B6E9D","#151A19","#2B6E9D","#4E8E79","#16377A","#151A19","#16377A","#B49A2D","#151A19"] },
    { img: "sunflowers.jpg", name: "Sunflowers", artist: "Vincent van Gogh",
      c: ["#197C6F","#DEBA58","#D0A23A","#197C6F","#D0A23A","#7C2E1C","#DEBA58","#C78F36","#DEBA58","#C78F36","#7C2E1C","#D0A23A","#C78F36","#DEBA58","#2A3915","#C78F36"] },
    { img: "scream.jpg", name: "The Scream", artist: "Edvard Munch",
      c: ["#B3532A","#DEAC5B","#C0A365","#B3532A","#C0A365","#2D2623","#2F747A","#1F3166","#2D2623","#2D2623","#2F747A","#2F747A","#2D2623","#2D2623","#1F3166","#2F747A"] },
    { img: "kiss.jpg", name: "The Kiss", artist: "Gustav Klimt",
      c: ["#CAA52D","#D4B645","#CFBB82","#CAA52D","#896D23","#A35DAA","#BB5733","#D4B645","#CFBB82","#BB5733","#A35DAA","#896D23","#7E8D61","#97A063","#896D23","#7E8D61"] },
    { img: "mona-lisa.jpg", name: "Mona Lisa", artist: "Leonardo da Vinci",
      c: ["#8F5A24","#95A146","#B3B750","#8F5A24","#95A146","#BA8F65","#BA8F65","#8F5A24","#8F5A24","#BA8F65","#290E25","#290E25","#290E25","#190E2B","#290E25","#190E2B"] }
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
