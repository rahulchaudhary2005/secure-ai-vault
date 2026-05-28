import { Shield, LogOut, UserCircle } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

function Navbar() {
    const { user, logout } = useAuth()
    const navigate = useNavigate()

    const handleLogout = () => {
        logout()
        navigate('/login')
    }

    return (
        <div className='w-full h-20 glass border-b border-white/10 flex items-center justify-between px-8'>
            <div className='flex items-center gap-3'>
                <Shield className='text-primary' size={32} />
                <h1 className='text-2xl font-bold text-primary'>Secure Privacy</h1>
            </div>

            <div className='flex items-center gap-4'>
                <div className='px-4 py-2 rounded-xl glass flex items-center gap-2 text-sm'>
                    <UserCircle size={18} />
                    {user?.email ?? 'Guest'}
                </div>
                <div className='px-4 py-2 rounded-xl glass text-sm'>AES-256</div>
                <div className='px-4 py-2 rounded-xl glass text-sm'>LOCAL-FIRST</div>
                <button
                    onClick={handleLogout}
                    className='flex items-center gap-2 px-4 py-2 rounded-xl glass text-sm hover:bg-white/10'
                >
                    <LogOut size={18} />
                    Sign out
                </button>
            </div>
        </div>
    )
}

export default Navbar