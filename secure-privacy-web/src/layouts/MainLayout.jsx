import Sidebar from '../components/ui/Sidebar'
import Navbar from '../components/ui/Navbar'

function MainLayout({ children }) {
    return (
        <div className='flex bg-dark min-h-screen cyber-grid'>
            <Sidebar />

            <div className='flex-1'>
                <Navbar />

                <div className='p-8'>
                    {children}
                </div>
            </div>
        </div>
    )
}

export default MainLayout