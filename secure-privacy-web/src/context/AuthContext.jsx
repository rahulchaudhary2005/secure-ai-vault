import React, {

    createContext,
    useContext,
    useState

} from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(
        localStorage.getItem("access_token") || null
    );

    const [user, setUser] = useState(() => {
        const storedUser = localStorage.getItem("user_data");
        return storedUser ? JSON.parse(storedUser) : null;
    });

    const login = (tokenData, userData) => {
        localStorage.setItem("access_token", tokenData);
        localStorage.setItem("user_data", JSON.stringify(userData));
        setToken(tokenData);
        setUser(userData);
    };

    const logout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user_data");
        setToken(null);
        setUser(null);
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                token,
                login,
                logout
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {

    return useContext(AuthContext);
};