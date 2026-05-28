import { motion } from 'framer-motion'

function Button({ children, onClick, className = '', disabled = false }) {
    return (
        <motion.button
            whileHover={!disabled ? { scale: 1.03 } : {}}
            whileTap={!disabled ? { scale: 0.97 } : {}}
            onClick={onClick}
            disabled={disabled}
            className={`
        px-6 py-3
        rounded-2xl
        bg-primary
        text-black
        font-semibold
        shadow-neon
        transition-all
        duration-300
        ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:opacity-90'}
        ${className}
      `}
        >
            {children}
        </motion.button>
    )
}

export default Button