import "./style.css";
import { addFavorite, deleteFavorite, getFavorites, getRandomCat } from "./api.js";

// Prvky na stránce
const catImage = document.querySelector("#cat-image");
const nextButton = document.querySelector("#next-btn");
const saveButton = document.querySelector("#save-btn");
const message = document.querySelector("#message");
const favoritesGrid = document.querySelector("#favorites");

// Kočka, která je právě zobrazená
let currentCat = null;

function showMessage(text) {
  message.textContent = text;
}

async function loadRandomCat() {
  showMessage("");
  try {
    currentCat = await getRandomCat();
    catImage.src = currentCat.url;
  } catch (error) {
    showMessage(error.message);
  }
}

async function saveCurrentCat() {
  if (!currentCat) return;
  try {
    await addFavorite(currentCat);
    showMessage("Uloženo ❤");
    await loadFavorites();
  } catch (error) {
    showMessage(error.message);
  }
}

// Vytvoří kartičku jedné oblíbené kočky
function createFavoriteCard(favorite) {
  const card = document.createElement("div");
  card.className = "card";

  const image = document.createElement("img");
  image.src = favorite.url;
  image.alt = "Oblíbená kočka";

  const deleteButton = document.createElement("button");
  deleteButton.textContent = "Smazat";
  deleteButton.addEventListener("click", async () => {
    await deleteFavorite(favorite.id);
    await loadFavorites();
  });

  card.append(image, deleteButton);
  return card;
}

async function loadFavorites() {
  try {
    const favorites = await getFavorites();
    favoritesGrid.replaceChildren(...favorites.map(createFavoriteCard));
  } catch (error) {
    showMessage(error.message);
  }
}

// Tlačítka
nextButton.addEventListener("click", loadRandomCat);
saveButton.addEventListener("click", saveCurrentCat);

// Po načtení stránky
loadRandomCat();
loadFavorites();