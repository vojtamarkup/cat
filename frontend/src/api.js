// Všechna volání backendu na jednom místě
const API = "/api";

export async function getRandomCat() {
  const response = await fetch(`${API}/cats/random`);
  if (!response.ok) throw new Error("Nepodařilo se načíst kočku");
  return response.json();
}

export async function getFavorites() {
  const response = await fetch(`${API}/favorites`);
  if (!response.ok) throw new Error("Nepodařilo se načíst oblíbené");
  return response.json();
}

export async function addFavorite(cat) {
  const response = await fetch(`${API}/favorites`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ cat_id: cat.id, url: cat.url }),
  });
  if (response.status === 409) throw new Error("Tahle kočka už je v oblíbených");
  if (!response.ok) throw new Error("Nepodařilo se uložit kočku");
  return response.json();
}

export async function deleteFavorite(id) {
  const response = await fetch(`${API}/favorites/${id}`, { method: "DELETE" });
  if (!response.ok) throw new Error("Nepodařilo se smazat kočku");
}