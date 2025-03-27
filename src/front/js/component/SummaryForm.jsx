import React, { useState } from "react";

export const SummaryForm = () => {
    const [text, setText] = useState("");
    const [file, setFile] = useState(null);
    const [summary, setSummary] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        if (file) formData.append("file", file);
        if (text) formData.append("text", text);

        const response = await fetch(process.env.BACKEND_URL+"/api/upload", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();
        setSummary(data.summary);
    };

    return (
        <div className="container mx-auto">
            <form className="form-control" onSubmit={handleSubmit}>
                <textarea
                    placeholder="Ingresa texto aquí"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    className="form-control my-3"
                />
                <input
                    type="file"
                    accept="application/pdf"
                    onChange={(e) => setFile(e.target.files[0])}
                    className="form-control mb-3"
                />
                <input className="btn btn-success" type="submit" />
            </form>
            {summary && <div className="mt-3 p-2"><h3>Resumen:</h3><p>{summary}</p></div>}
        </div>
    );
};