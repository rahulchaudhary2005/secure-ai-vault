import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { useAuth } from '../context/AuthContext'
import { loginUser } from '../features/auth/services/authService'

function Login() {
    const { token, login } = useAuth()
    const navigate = useNavigate()
    const [form, setForm] = useState({
        email: '',
        password: ''
    })
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        if (token) {
            navigate('/')
        }
    }, [token, navigate])

    const handleChange = (event) => {
        const { name, value } = event.target
        setForm((state) => ({
            ...state,
            [name]: value
        }))
    }

    const handleSubmit = async (event) => {
        event.preventDefault()
        setLoading(true)

        try {
            const response = await loginUser(form)
            
            if (response.success) {
                login(response.access_token, response.user || { email: form.email })
                toast.success('Welcome back!')
                navigate('/')
            } else {
                toast.error(response.detail || 'Login failed')
            }
        } catch (error) {
            console.error('Login failed', error)
            const message = error.response?.data?.detail || 'Login failed. Check your credentials.'
            toast.error(message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className='min-h-screen flex items-center justify-center cyber-grid p-6'>
            <div className='max-w-md w-full glass neon-border rounded-3xl p-10 shadow-xl'>
                <h1 className='text-4xl font-bold mb-4 text-primary'>Welcome Back</h1>
                <p className='text-gray-400 mb-8'>Secure vault access with email and password.</p>

                <form onSubmit={handleSubmit} className='space-y-6'>
                    <label className='block'>
                        <span className='text-gray-300'>Email</span>
                        <input
                            name='email'
                            type='email'
                            value={form.email}
                            onChange={handleChange}
                            required
                            className='mt-2 w-full rounded-2xl border border-white/10 bg-black/20 px-4 py-3 text-white outline-none transition focus:border-primary'
                        />
                    </label>

                    <label className='block'>
                        <span className='text-gray-300'>Password</span>
                        <input
                            name='password'
                            type='password'
                            value={form.password}
                            onChange={handleChange}
                            required
                            className='mt-2 w-full rounded-2xl border border-white/10 bg-black/20 px-4 py-3 text-white outline-none transition focus:border-primary'
                        />
                    </label>

                    <button
                        type='submit'
                        disabled={loading}
                        className='w-full rounded-2xl bg-primary px-5 py-3 text-black font-semibold transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-60'
                    >
                        {loading ? 'Signing in...' : 'Sign in'}
                    </button>
                </form>

                <p className='mt-6 text-center text-gray-400'>
                    New to the vault?{' '}
                    <Link to='/register' className='text-primary hover:text-cyan-300'>Create account</Link>
                </p>
            </div>
        </div>
    )
}

export default Login
