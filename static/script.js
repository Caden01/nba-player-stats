const $search = $("#search-input");
const $searchBtn = $("#search-btn");
const $suggestions = $(".suggestions");

async function searchSuggestion(evt) {
  const res = await axios.get("/suggestions");
  $suggestions.html("");

  for (let player of res.data.players) {
    if (player.toLowerCase().includes(evt.target.value.toLowerCase())) {
      $suggestions.append(`<li class="list-group-item">${player}</li>`);
    }
  }

  $(".list-group-item").on("click", (evt) => {
    $search.val(`${evt.target.innerText}`);
  });

  $("body").on("click", (evt) => {
    $suggestions.html("");
  });
}

async function sendSearchValue(evt) {
  val = $search.val();
  const res = await axios.post(`/player/${val}`);
  console.log(res);
}

$search.on("keyup", searchSuggestion);
$searchBtn.on("click", sendSearchValue);
