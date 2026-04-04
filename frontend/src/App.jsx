import { useState } from "react";
import { motion } from "framer-motion";
import { Search } from "lucide-react";

export default function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    if (!query.trim()) return;

    const res = await fetch(`http://localhost:8000/search?query=${query}`);
    if (!res.ok) return;
    const json_res = await res.json();
    const results = json_res.results;
    console.log(results);
    setResults(results);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black text-white flex flex-col items-center px-4">
      {/* Header */}
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-5xl font-extrabold mt-20 tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600"
      >
        Nebula Search
      </motion.h1>

      {/* Search Box */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="mt-10 w-full max-w-2xl relative"
      >
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          placeholder="Search the universe..."
          className="w-full p-4 pl-12 rounded-2xl bg-white/10 backdrop-blur-lg border border-white/20 focus:outline-none focus:ring-2 focus:ring-purple-500"
        />
        <Search className="absolute left-4 top-4 opacity-70" />
      </motion.div>

      {/* Results */}
      <div className="mt-12 w-full max-w-3xl space-y-6">
        {results.map((result, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="p-6 rounded-2xl bg-white/5 border border-white/10 hover:border-purple-500 hover:bg-white/10 transition-all"
          >
            <a
              href={result.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xl font-semibold text-purple-400 hover:underline"
            >
              {result.url}
            </a>
            <p
              className="text-gray-300 mt-2"
              dangerouslySetInnerHTML={{ __html: result.content }}
            />
          </motion.div>
        ))}
      </div>

      {/* Footer */}
      <div className="mt-auto mb-6 text-sm text-gray-500">
        Built with ❤️ by Mayank
      </div>
    </div>
  );
}
