import { useState, useEffect } from "react";

import { askAI } from "../services/aiChatService";
import { getUploadedFiles } from "../services/uploadService";

export default function AIChat() {

    const [message, setMessage] =
        useState("");

    const [response, setResponse] =
        useState("");

    const [availableFiles, setAvailableFiles] =
        useState([]);

    const [selectedFiles, setSelectedFiles] =
        useState([]);

    const [loading, setLoading] =
        useState(false);

    const handleAsk = async () => {

        try {

            setLoading(true);

            const res = await askAI(
                message,
                selectedFiles
            );

            const aiResp = res?.response;

            if (aiResp && aiResp.answer) {

                setResponse(aiResp.answer);

            } else if (aiResp) {

                setResponse(JSON.stringify(aiResp, null, 2));

            } else {

                setResponse("No response returned");

            }

        } catch (error) {

            console.error(error);

            setResponse(
                "AI request failed"
            );

        } finally {

            setLoading(false);
        }
    };

    useEffect(() => {

        const loadFiles = async () => {

            try {

                const res = await getUploadedFiles();

                setAvailableFiles(res.files || []);

            } catch (e) {

                console.error(e);

            }

        };

        loadFiles();

    }, []);

    const toggleFile = (filename) => {

        setSelectedFiles((prev) => {

            if (prev.includes(filename)) {

                return prev.filter((f) => f !== filename);

            }

            return [...prev, filename];

        });

    };

    return (

        <div className="p-6">

            <h1 className="text-2xl font-bold mb-4">

                Secure AI Chat

            </h1>

            <textarea

                value={message}

                onChange={(e) =>
                    setMessage(e.target.value)
                }

                className="border p-4 w-full h-40"
            />

            <button

                onClick={handleAsk}

                disabled={loading}

                className="bg-blue-600 text-white px-4 py-2 rounded mt-4"
            >

                {

                    loading
                        ? "Thinking..."
                        : "Ask AI"
                }

            </button>

            <div className="mt-6">

                <h2 className="font-bold">

                    AI Response

                </h2>

                <p>{response}</p>

                <div className="mt-6">

                    <h3 className="font-semibold">Select Uploaded Files (optional)</h3>

                    <div className="mt-2">

                        {availableFiles.length === 0 && (

                            <p className="text-sm text-gray-500">No uploaded files found.</p>

                        )}

                        {availableFiles.map((f) => (

                            <div key={f.filename} className="flex items-center">

                                <input

                                    type="checkbox"

                                    checked={selectedFiles.includes(f.filename)}

                                    onChange={() => toggleFile(f.filename)}

                                />

                                <span className="ml-2">{f.filename}</span>

                            </div>

                        ))}

                    </div>

                </div>

            </div>

        </div>
    );
}