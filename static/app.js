class BoggleGame {
  constructor(boarId, seconds = 60) {
    this.seconds = seconds;
    this.board = $("#" + boarId);

    this.score = 0;
    this.words = new Set();

    this.showTimer();
    this.timer = setInterval(this.watch.bind(this), 1000);
    $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
  }

  showWord(word) {
    $(".words", this.board).append($("<li>", { text: word }));
  }

  showScore() {
    $(".score", this.board).text(this.score);
  }

  showMessage(message, cls) {
    $(".message", this.board)
      .text(message)
      .removeClass()
      .addClass(`message ${cls}`);
  }

  async handleSubmit(event) {
    event.preventDefault();
    console.log(event);
    const $word = $(".word", this.board);
    console.log($word);
    let word = $word.val();

    if (!word) return;

    if (this.words.has(word)) {
      this.showMessage(`${word} already been found`, "err");
      return;
    }

    const res = await axios.get("/check-word", { params: { word: word } });

    if (res.data.result === "not-word") {
      this.showMessage(`${word} not a valid word`, "err");
    } else if (res.data.result === "not-on-board") {
      this.showMessage(`${word} not on this board`, "err");
    } else {
      this.showWord(word);
      this.words.add(word);
      this.showMessage(`Added: ${word}`, "ok");
      this.score += word.length;
      this.showScore();
    }

    $word.val("");
  }

  showTimer() {
    $(".timer", this.board).text(this.seconds);
  }

  async watch() {
    this.seconds -= 1;
    this.showTimer();

    if (this.seconds === 0) {
      clearInterval(this.timer);
      await this.scoreGame();
    }
  }

  async scoreGame() {
    $(".add-word", this.board).hide();

    const res = await axios.post("/post-score", { score: this.score });

    if (res.data.brokeRecord) {
      this.showMessage(`New Record: ${this.score}`, "ok");
    } else {
      this.showMessage(`Final Score: ${this.score}`, "ok");
    }
  }
}
