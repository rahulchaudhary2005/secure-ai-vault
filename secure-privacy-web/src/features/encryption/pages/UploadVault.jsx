// import { useState } from "react";

// import {

//     uploadDocument

// } from "../services/uploadService";

// export default function UploadVault() {

//     const [file, setFile] =
//         useState(null);

//     const [status, setStatus] =
//         useState("");

//     const handleUpload = async () => {

//         if (!file) return;

//         setStatus("Uploading...");

//         const response =
//             await uploadDocument(file);

//         setStatus(

//             response.message
//         );
//     };

//     return (

//         <div>

//             <h1>
//                 Upload Secure Document
//             </h1>

//             <input

//                 type="file"

//                 onChange={(e) =>

//                     setFile(
//                         e.target.files[0]
//                     )
//                 }
//             />

//             <button onClick={handleUpload}>

//                 Upload

//             </button>

//             <p>{status}</p>

//         </div>
//     );
// }

import { useState } from 'react'
import { Link } from 'react-router-dom'
import MainLayout from '../../../layouts/MainLayout'
import Button from '../../../components/ui/Button'
import { uploadDocument } from '../services/uploadService'

export default function UploadVault() {
    const [files, setFiles] = useState([])
    const [status, setStatus] = useState('')
    const [loading, setLoading] = useState(false)

    const handleUpload = async () => {
        try {
            if (!files.length) {
                setStatus('Please select files to upload.')
                return
            }

            setLoading(true)
            setStatus('Uploading secure files...')

            const response = await uploadDocument(files)
            setStatus(response.message || 'Files uploaded successfully.')
        } catch (error) {
            console.error(error)
            setStatus(error?.response?.data?.detail || 'Upload failed. Please try again.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <MainLayout>
            <div className='max-w-4xl mx-auto p-6'>
                <div className='glass border border-white/10 rounded-[32px] p-8 shadow-xl'>
                    <div className='mb-8'>
                        <p className='text-sm uppercase tracking-[0.3em] text-gray-400 mb-2'>Encryption Center</p>
                        <div className='flex flex-col gap-3 md:flex-row md:items-end md:justify-between'>
                            <div>
                                <h1 className='text-3xl font-bold text-white'>Upload Files for Encryption</h1>
                                <p className='mt-2 text-sm text-gray-300'>Select one or more files to encrypt and store safely in your secure vault.</p>
                            </div>
                            <Link to='/encrypt' className='text-sm text-primary hover:underline'>Back to Encrypt</Link>
                        </div>
                    </div>

                    <div className='flex flex-col gap-5'>
                        <div>
                            <label htmlFor='upload' className='block text-sm font-medium text-gray-200 mb-2'>Choose files</label>
                            <input
                                id='upload'
                                type='file'
                                multiple
                                onChange={(e) => setFiles(Array.from(e.target.files || []))}
                                className='block w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-gray-100 file:mr-4 file:rounded-full file:border-0 file:bg-primary file:px-4 file:py-2 file:text-black focus:outline-none focus:ring-2 focus:ring-primary/60'
                            />
                            {files.length > 0 && (
                                <p className='mt-3 text-sm text-gray-300'>{files.length} file(s) ready to upload</p>
                            )}
                        </div>

                        <Button onClick={handleUpload} className='w-full'>
                            {loading ? 'Uploading...' : 'Upload Secure Files'}
                        </Button>

                        {status && <p className='text-sm text-gray-200'>{status}</p>}
                    </div>
                </div>
            </div>
        </MainLayout>
    )
}
