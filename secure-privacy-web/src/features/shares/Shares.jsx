import React, { useEffect, useState } from 'react'
import apiClient from '../../services/apiClient'

const Shares = () => {
    const [view, setView] = useState('received') // 'received' | 'sent'
    const [loading, setLoading] = useState(false)
    const [shares, setShares] = useState([])
    const [error, setError] = useState(null)

    useEffect(() => {
        const fetchShares = async () => {
            try {
                setLoading(true)
                setError(null)

                const path = view === 'sent' ? '/api/secure-share/shares/sent' : '/api/secure-share/shares/received'
                const res = await apiClient.get(path)

                setShares(res.data.shares || [])
            } catch (err) {
                setError(err?.response?.data?.detail || err.message)
            } finally {
                setLoading(false)
            }
        }

        fetchShares()
    }, [view])

    return (
        <div className="p-6">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold">Shares</h2>
                <div className="flex gap-2">
                    <button
                        className={`px-3 py-1 rounded ${view === 'received' ? 'bg-primary text-black' : 'bg-gray-700'}`}
                        onClick={() => setView('received')}
                    >Received</button>
                    <button
                        className={`px-3 py-1 rounded ${view === 'sent' ? 'bg-primary text-black' : 'bg-gray-700'}`}
                        onClick={() => setView('sent')}
                    >Sent</button>
                </div>
            </div>

            {loading && <div>Loading...</div>}

            {error && <div className="text-red-400">{error}</div>}

            {!loading && !error && (
                <div className="bg-gray-800/30 rounded-lg p-4">
                    {shares.length === 0 ? (
                        <div className="text-gray-400">No shares found.</div>
                    ) : (
                        <div className="grid grid-cols-1 gap-3">
                            {shares.map((s) => (
                                <div key={s.share_id} className="flex items-center justify-between p-3 bg-gray-900/50 rounded-lg">
                                    <div>
                                        <div className="text-sm text-gray-400">{view === 'sent' ? 'To' : 'From'}: <span className="text-white font-semibold">{view === 'sent' ? s.recipient_email : s.sender_email}</span></div>
                                        <div className="text-sm text-gray-300">{s.filename || s.original_filename}</div>
                                        <div className="text-xs text-gray-500">Share ID: <span className="font-mono">{s.share_id}</span></div>
                                    </div>

                                    <div className="text-right text-xs text-gray-400">
                                        <div>{s.size ? `${(s.size / 1024 / 1024).toFixed(2)} MB` : ''}</div>
                                        <div className="mt-2">{s.status}</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}

export default Shares
