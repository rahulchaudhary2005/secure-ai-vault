import { NavLink } from 'react-router-dom'
import {
    LayoutDashboard,
    Lock,
    Unlock,
    Settings,
    Upload,
    Search,
    MessageCircle,
    Brain,
} from 'lucide-react'

const sections = [
    {
        title: 'Encryption',
        items: [
            {
                title: 'Encrypt',
                icon: <Lock size={20} />,
                path: '/encrypt',
            },
            {
                title: 'Upload File',
                icon: <Upload size={20} />,
                path: '/upload-vault',
            },
            {
                title: 'Decrypt',
                icon: <Unlock size={20} />,
                path: '/decrypt',
            },
        ],
    },
    {
        title: 'AI & Search',
        items: [
            {
                title: 'Semantic Search',
                icon: <Search size={20} />,
                path: '/semantic-search',
            },
            {
                title: 'AI Assistant',
                icon: <Brain size={20} />,
                path: '/ai-assistant',
            },
            {
                title: 'AI Chat',
                icon: <MessageCircle size={20} />,
                path: '/ai-chat',
            },
        ],
    },
    {
        title: 'General',
        items: [
            {
                title: 'Dashboard',
                icon: <LayoutDashboard size={20} />,
                path: '/',
            },
            {
                title: 'Settings',
                icon: <Settings size={20} />,
                path: '/settings',
            },
        ],
    },
]

function Sidebar() {
    return (
        <div className='w-[280px] min-h-screen glass border-r border-white/10 p-6'>
            <div className='text-3xl font-bold text-primary mb-8'>CipherX</div>

            {sections.map((section) => (
                <div key={section.title} className='mb-6'>
                    <p className='text-xs uppercase tracking-[0.3em] text-gray-400 mb-3'>
                        {section.title}
                    </p>
                    <div className='flex flex-col gap-2'>
                        {section.items.map((menu) => (
                            <NavLink
                                key={menu.title}
                                to={menu.path}
                                className={({ isActive }) =>
                                    `flex items-center gap-3 p-4 rounded-2xl transition-all duration-300 text-sm font-medium ${
                                        isActive
                                            ? 'bg-primary text-black shadow-neon'
                                            : 'text-gray-200 hover:bg-white/10'
                                    }`
                                }
                            >
                                {menu.icon}
                                {menu.title}
                            </NavLink>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    )
}

export default Sidebar