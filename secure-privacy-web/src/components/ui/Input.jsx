function Input({ type = 'text', placeholder, value, onChange }) {
    return (
        <input
            type={type}
            placeholder={placeholder}
            value={value}
            onChange={onChange}
            className='
        w-full
        p-4
        rounded-2xl
        glass
        neon-border
        outline-none
        text-white
        placeholder:text-gray-400
      '
        />
    )
}

export default Input