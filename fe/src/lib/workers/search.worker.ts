import TrieSearch from "trie-search";

let trie: any = null;
let allData: any[] = [];
const cache = new Map<string, any[]>();

self.onmessage = (e: MessageEvent) => {
    const { type, payload } = e.data;

    if (type === "init") {
        trie = new TrieSearch("title", { ignoreCase: true, cache: true });
        trie.addAll(payload);
        allData = payload;
        cache.clear();
        self.postMessage({ type: "ready" });
    } else if (type === "search") {
        if (trie !== null) {
            if (payload.trim().length === 0) {
                self.postMessage({ type: "results", payload: allData });
                return;
            }

            if (cache.has(payload)) {
                self.postMessage({ type: "results", payload: cache.get(payload) });
            } else {
                const results = trie.search(payload);

                cache.set(payload, results);

                self.postMessage({ type: "results", payload: results });
            }
        }
    }
};
