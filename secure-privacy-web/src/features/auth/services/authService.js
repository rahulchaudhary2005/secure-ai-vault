import apiClient from "../../../services/apiClient";

export const registerUser = async (data) => {

    const response = await apiClient.post(

        "/api/auth/register",

        data
    );

    return response.data;
};

export const loginUser = async (data) => {

    const response = await apiClient.post(

        "/api/auth/login",

        data
    );

    return response.data;
};

export const verifyOTP = async (data) => {

    const response = await apiClient.post(

        "/api/verify/otp",

        data
    );

    return response.data;
};