import apiClient from "../../../services/apiClient";

export const uploadDocument = async (
    files
) => {

    const formData = new FormData();

    files.forEach((file) => {

        formData.append(
            "files",
            file
        );
    });

    const response =
        await apiClient.post(

            "/api/upload/",

            formData,

            {

                headers: {

                    "Content-Type":
                        "multipart/form-data"
                }
            }
        );

    return response.data;
};

export const getUploadedFiles = async () => {

    const response = await apiClient.get(

        "/api/upload/files"
    );

    return response.data;
};