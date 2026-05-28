import { Routes, Route } from 'react-router-dom'
import Dashboard from '../pages/Dashboard'
import Encrypt from '../features/encryption/pages/Encrypt'
import Decrypt from '../features/encryption/pages/Decrypt'
import Settings from '../pages/Settings'
import NotFound from '../pages/NotFound'
import AIChat from '../features/encryption/pages/AIChat'
import UploadVault from '../features/encryption/pages/UploadVault'
import Login from '../pages/Login'
import Register from '../pages/Register'
import ProtectedRoute from '../components/auth/ProtectedRoute'

function AppRoutes() {
    return (
        <Routes>
            <Route
                path='/'
                element={
                    <ProtectedRoute>
                        <Dashboard />
                    </ProtectedRoute>
                }
            />
            <Route
                path='/encrypt'
                element={
                    <ProtectedRoute>
                        <Encrypt />
                    </ProtectedRoute>
                }
            />
            <Route
                path='/decrypt'
                element={
                    <ProtectedRoute>
                        <Decrypt />
                    </ProtectedRoute>
                }
            />
            <Route
                path='/settings'
                element={
                    <ProtectedRoute>
                        <Settings />
                    </ProtectedRoute>
                }
            />
            <Route
                path='/ai-chat'
                element={
                    <ProtectedRoute>
                        <AIChat />
                    </ProtectedRoute>
                }
            />
            <Route
                path='/upload-vault'
                element={
                    <ProtectedRoute>
                        <UploadVault />
                    </ProtectedRoute>
                }
            />
            <Route path='/login' element={<Login />} />
            <Route path='/register' element={<Register />} />
            <Route path='*' element={<NotFound />} />
        </Routes>
    )
}

export default AppRoutes