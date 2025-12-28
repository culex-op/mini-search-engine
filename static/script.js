async function chat() {
    const q = document.getElementById("chatQuery").value.trim();
    const ansDiv = document.getElementById("chatAnswer");

    ansDiv.innerHTML = "Thinking...";

    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            question: q,
            top_k: 3
        })
    });

    const text = await res.text();   // 👈 IMPORTANT
    console.log("RAW RESPONSE:", text);

    try {
        const data = JSON.parse(text);
        ansDiv.innerHTML = data.answer ?? text;
    } catch {
        ansDiv.innerHTML = text;
    }
}

async function search() {
    const query = document.getElementById("query").value;
    const resultsDiv = document.getElementById("results");

    resultsDiv.innerHTML = "Searching...";

    const response = await fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, top_k: 10 })
    });

    const data = await response.json();
    resultsDiv.innerHTML = "";

    if (data.results.length === 0) {
        resultsDiv.innerHTML = "<p>No results found.</p>";
        return;
    }

    data.results.forEach(item => {
        const div = document.createElement("div");
        div.innerHTML = `
            <p><strong>Document ${item.doc_id}</strong></p>
            <p>${item.text}</p>
            <small>Score: ${item.score.toFixed(4)}</small>
            <hr>
        `;
        resultsDiv.appendChild(div);
    });
}

async function addDocument() {
    const docId = parseInt(document.getElementById("docId").value);
    const text = document.getElementById("docText").value;

    await fetch("/documents", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ doc_id: docId, text })
    });

    alert("Document added");
}

async function saveIndex() {
    await fetch("/save", { method: "POST" });
    alert("Index saved");
}

async function loadIndex() {
    await fetch("/load", { method: "POST" });
    alert("Index loaded");
    viewDocuments();   
}

async function viewDocuments() {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "Loading documents...";

    const response = await fetch("/documents");
    const docs = await response.json();

    resultsDiv.innerHTML = "";

    const entries = Object.entries(docs);

    if (entries.length === 0) {
        resultsDiv.innerHTML = "<p>No documents indexed.</p>";
        return;
    }

    entries.forEach(([docId, text]) => {
        const div = document.createElement("div");
        div.innerHTML = `
            <p><strong>Document ${docId}</strong></p>
            <p>${text}</p>
            <hr>
        `;
        resultsDiv.appendChild(div);
    });
}


