import { afterEach, expect, test, vi } from "vitest";
import { addFavorite, getRandomCat } from "./api.js";

// Podvrhne fetch: vrátí odpověď s daným stavem a daty
function mockFetch(status, body) {
  const fetchMock = vi.fn().mockResolvedValue({
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
  });
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

// Po každém testu vrať skutečný fetch
afterEach(() => {
  vi.unstubAllGlobals();
});

test("getRandomCat vrátí kočku", async () => {
  mockFetch(200, { id: "abc", url: "https://example.com/abc.jpg" });

  const cat = await getRandomCat();

  expect(cat).toEqual({ id: "abc", url: "https://example.com/abc.jpg" });
});

test("getRandomCat vyhodí chybu, když backend selže", async () => {
  mockFetch(502, {});

  await expect(getRandomCat()).rejects.toThrow("Nepodařilo se načíst kočku");
});

test("addFavorite pošle správná data", async () => {
  const fetchMock = mockFetch(201, {});

  await addFavorite({ id: "abc", url: "https://example.com/abc.jpg" });

  expect(fetchMock).toHaveBeenCalledWith(
    "/api/favorites",
    expect.objectContaining({
      method: "POST",
      body: JSON.stringify({ cat_id: "abc", url: "https://example.com/abc.jpg" }),
    }),
  );
});

test("addFavorite hlásí duplicitní kočku", async () => {
  mockFetch(409, {});

  await expect(addFavorite({ id: "abc", url: "x" })).rejects.toThrow("Tahle kočka už je v oblíbených");
});