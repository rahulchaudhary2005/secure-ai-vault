import MainLayout from '../layouts/MainLayout'

import { motion } from 'framer-motion'

import {
    ShieldCheck,
    Lock,
    Database,
    Key,
    Brain,
    FileText,
    Activity,
    Cpu
} from 'lucide-react'

import {
    useEffect,
    useState
} from 'react'

import { useAuth } from '../context/AuthContext'

import { useNavigate } from 'react-router-dom'
import apiClient from '../services/apiClient'

function Dashboard() {
    const navigate = useNavigate()
    const { user } = useAuth()
    const userEmail = user?.email || user?.username || 'User'
    const [stats, setStats] = useState({
        total_documents: 0,
        total_vectors: 0,
        ai_requests: 0,
        active_tasks: 0
    })
    const [documents, setDocuments] = useState([])

    useEffect(() => {
        loadDashboard()
    }, [])

    const loadDashboard = async () => {
        try {
            const [statsResponse, vaultResponse] = await Promise.all([
                apiClient.get('/api/dashboard/stats'),
                apiClient.get('/api/vault/documents')
            ])

            setStats(statsResponse.data)
            setDocuments(
                Array.isArray(vaultResponse?.data?.documents)
                    ? vaultResponse.data.documents
                    : []
            )
        } catch (error) {
            console.error('Dashboard Error:', error)
            if (error?.response?.status === 401) {
                navigate('/login')
            }
        }
    }

    const cards = [
        {
            title: 'AES-256 Encryption',
            icon: <Lock size={40} />,
            description: 'Military-grade local encryption system.'
        },
        {
            title: 'Secure Storage',
            icon: <Database size={40} />,
            description: `${stats.total_documents} encrypted vault documents.`
        },
        {
            title: 'AI Vector Database',
            icon: <Brain size={40} />,
            description: `${stats.total_vectors} semantic vectors indexed.`
        },
        {
            title: 'AI Processing',
            icon: <Cpu size={40} />,
            description: `${stats.active_tasks} active AI tasks.`
        },
        {
            title: 'OCR Intelligence',
            icon: <FileText size={40} />,
            description: 'Advanced OCR + semantic extraction.'
        },
        {
            title: 'AI Analytics',
            icon: <Activity size={40} />,
            description: `${stats.ai_requests} AI requests processed.`
        },
        {
            title: 'Key Protection',
            icon: <Key size={40} />,
            description: 'PBKDF2 password-based key derivation.'
        },
        {
            title: 'Privacy First',
            icon: <ShieldCheck size={40} />,
            description: 'No cloud. No tracking. Fully local.'
        }
    ]

    return (
        <MainLayout>
            <div className='mb-10'>
                <h1 className='text-5xl font-bold mb-4'>
                    Cyber Security Dashboard
                </h1>
                <p className='text-gray-400 text-lg'>
                    Enterprise AI cybersecurity and privacy platform.
                </p>
                {userEmail && (
                    <p className='text-primary text-sm mt-2'>
                        Logged in and viewing vault data.
                    </p>
                )}
            </div>

            <div className='grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6'>
                {cards.map((card, index) => (
                    <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className='glass neon-border rounded-3xl p-6 hover:scale-[1.02] transition-all duration-300'
                    >
                        <div className='text-primary mb-5'>{card.icon}</div>
                        <h2 className='text-2xl font-bold mb-3'>{card.title}</h2>
                        <p className='text-gray-400'>{card.description}</p>
                    </motion.div>
                ))}
            </div>

            <div className='mt-10 glass neon-border rounded-3xl p-6'>
                <div className='flex flex-col gap-4 md:flex-row md:items-center md:justify-between'>
                    <div>
                        <h2 className='text-2xl font-bold'>Vault Documents</h2>
                        <p className='text-gray-400'>Real documents stored for your account.</p>
                    </div>
                    <div className='rounded-2xl bg-white/5 px-4 py-3 text-sm text-primary'>
                        {documents.length} documents synced
                    </div>
                </div>

                {documents.length > 0 ? (
                    <div className='mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3'>
                        {documents.map((doc, index) => (
                            <div key={index} className='glass rounded-3xl p-4'>
                                <h3 className='font-semibold mb-2 text-white'>{doc.filename}</h3>
                                <p className='text-gray-400 text-sm'>Vector collection: {doc.vector_collection}</p>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p className='mt-6 text-gray-400'>No vault documents found yet. Upload your first secure file.</p>
                )}
            </div>
        </MainLayout>
    )
}

export default Dashboard