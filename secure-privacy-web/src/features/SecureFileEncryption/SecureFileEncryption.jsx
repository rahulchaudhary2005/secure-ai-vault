import React, { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { Upload, Mail, Lock, Eye, EyeOff, Check, X, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';

/**
 * Secure File Encryption Component
 * Industry-grade encryption with dual-email OTP verification
 */

const SecureFileEncryption = () => {
    // =========================
    // STATE MANAGEMENT
    // =========================

    const [step, setStep] = useState('intro');
    const fileInputRef = useRef(null);

    // Step 1: Email Verification
    const [senderEmail, setSenderEmail] = useState('');
    const [recipientEmail, setRecipientEmail] = useState('');
    const [emailValidation, setEmailValidation] = useState({
        sender: null,
        recipient: null
    });

    // Step 2: OTP Verification
    const [senderSessionId, setSenderSessionId] = useState('');
    const [recipientSessionId, setRecipientSessionId] = useState('');
    const [senderOTP, setSenderOTP] = useState('');
    const [recipientOTP, setRecipientOTP] = useState('');
    const [otpVerification, setOtpVerification] = useState({
        sender: null,
        recipient: null
    });

    // Step 3: File Upload & Encryption
    const [selectedFile, setSelectedFile] = useState(null);
    const [encryptionPassword, setEncryptionPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [passwordStrength, setPasswordStrength] = useState(0);
    const [filePreview, setFilePreview] = useState(null);

    // Loading & Status
    const [loading, setLoading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);

    // Success
    const [shareId, setShareId] = useState('');
    const [encryptedFileInfo, setEncryptedFileInfo] = useState(null);

    // =========================
    // UTILITY FUNCTIONS
    // =========================

    const validateEmail = (email) => {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    };

    const calculatePasswordStrength = (password) => {
        let strength = 0;
        if (password.length >= 8) strength += 25;
        if (password.length >= 12) strength += 25;
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength += 25;
        if (/\d/.test(password) && /[!@#$%^&*]/.test(password)) strength += 25;
        return Math.min(strength, 100);
    };

    const getPasswordStrengthColor = (strength) => {
        if (strength < 30) return 'bg-red-500';
        if (strength < 60) return 'bg-yellow-500';
        if (strength < 85) return 'bg-blue-500';
        return 'bg-green-500';
    };

    // =========================
    // API CALLS
    // =========================

    const handleInitEncryption = async () => {
        try {
            if (!validateEmail(senderEmail)) {
                toast.error('Invalid sender email');
                return;
            }

            if (!validateEmail(recipientEmail)) {
                toast.error('Invalid recipient email');
                return;
            }

            if (senderEmail === recipientEmail) {
                toast.error('Sender and recipient must be different');
                return;
            }

            setLoading(true);

            const response = await fetch(
                'http://localhost:8000/api/secure-share/encrypt/init',
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        sender_email: senderEmail,
                        recipient_email: recipientEmail,
                        file_description: 'Secure file transfer'
                    })
                }
            );

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to initialize encryption');
            }

            const data = await response.json();

            setSenderSessionId(data.sender_session_id);
            setRecipientSessionId(data.recipient_session_id);

            toast.success(
                'OTP codes sent to both emails. Both must verify.'
            );

            setStep('otp-verification');
            setEmailValidation({
                sender: true,
                recipient: true
            });

        } catch (error) {
            toast.error(error.message || 'Failed to initialize encryption');
        } finally {
            setLoading(false);
        }
    };

    const handleVerifyOTP = async (role) => {
        try {
            const sessionId = (
                role === 'sender' ? senderSessionId : recipientSessionId
            );

            const otpCode = (
                role === 'sender' ? senderOTP : recipientOTP
            );

            const email = (
                role === 'sender' ? senderEmail : recipientEmail
            );

            if (!otpCode || otpCode.length !== 6) {
                toast.error('Please enter valid 6-digit OTP');
                return;
            }

            setLoading(true);

            const response = await fetch(
                'http://localhost:8000/api/secure-share/encrypt/verify-otp',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'user-email': email,
                        'user-role': role
                    },
                    body: JSON.stringify({
                        session_id: sessionId,
                        otp_code: otpCode
                    })
                }
            );

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'OTP verification failed');
            }

            const data = await response.json();

            setOtpVerification(prev => ({
                ...prev,
                [role]: {
                    verified: true,
                    token: data.access_token
                }
            }));

            toast.success(`${role} OTP verified successfully`);

        } catch (error) {
            toast.error(error.message || 'OTP verification failed');
        } finally {
            setLoading(false);
        }
    };

    const handleFileSelect = (e) => {
        const file = e.target.files?.[0];

        if (!file) return;

        setSelectedFile(file);

        // Generate preview
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (event) => {
                setFilePreview(event.target?.result);
            };
            reader.readAsDataURL(file);
        } else {
            setFilePreview(null);
        }

        toast.success(`File selected: ${file.name}`);
    };

    const handleUploadAndEncrypt = async () => {
        try {
            if (!selectedFile) {
                toast.error('Please select a file');
                return;
            }

            if (!encryptionPassword) {
                toast.error('Please enter encryption password');
                return;
            }

            if (calculatePasswordStrength(encryptionPassword) < 50) {
                toast.error('Password is too weak');
                return;
            }

            if (
                !otpVerification.sender?.verified
                || !otpVerification.recipient?.verified
            ) {
                toast.error('Both users must verify OTP first');
                return;
            }

            setLoading(true);

            const formData = new FormData();
            formData.append('file', selectedFile);

            const response = await fetch(
                'http://localhost:8000/api/secure-share/encrypt/upload',
                {
                    method: 'POST',
                    headers: {
                        'sender-email': senderEmail,
                        'recipient-email': recipientEmail,
                        'password': encryptionPassword,
                        'authorization': (
                            `Bearer ${otpVerification.sender.token}`
                        )
                    },
                    body: formData
                }
            );

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Upload failed');
            }

            const data = await response.json();

            setShareId(data.share_id);
            setEncryptedFileInfo(data.file_info);

            toast.success('File encrypted and uploaded successfully!');

            setStep('success');

        } catch (error) {
            toast.error(error.message || 'Upload and encryption failed');
        } finally {
            setLoading(false);
        }
    };

    // =========================
    // RENDER METHODS
    // =========================

    const renderIntroStep = () => (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gradient-to-br from-blue-900/30 to-purple-900/30 
                 backdrop-blur-xl border border-blue-500/20 rounded-2xl p-8"
        >
            <div className="text-center mb-8">
                <div className="inline-block p-4 bg-blue-500/20 rounded-xl mb-4">
                    <Lock className="w-8 h-8 text-blue-400" />
                </div>
                <h2 className="text-3xl font-bold text-transparent 
                      bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
                    Secure File Encryption
                </h2>
                <p className="text-gray-400 mt-2">
                    Share encrypted files with dual-email OTP verification
                </p>
            </div>

            <div className="space-y-4 mb-8">
                <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                        <Mail className="w-4 h-4 inline mr-2 text-blue-400" />
                        Your Email (Sender)
                    </label>
                    <input
                        type="email"
                        value={senderEmail}
                        onChange={(e) => setSenderEmail(e.target.value)}
                        className="w-full bg-gray-800/50 border border-gray-600/30 
                      rounded-lg px-4 py-3 text-white focus:outline-none 
                      focus:border-blue-500/50 transition"
                        placeholder="your@email.com"
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                        <Mail className="w-4 h-4 inline mr-2 text-purple-400" />
                        Recipient Email
                    </label>
                    <input
                        type="email"
                        value={recipientEmail}
                        onChange={(e) => setRecipientEmail(e.target.value)}
                        className="w-full bg-gray-800/50 border border-gray-600/30 
                      rounded-lg px-4 py-3 text-white focus:outline-none 
                      focus:border-purple-500/50 transition"
                        placeholder="recipient@email.com"
                    />
                </div>
            </div>

            <button
                onClick={handleInitEncryption}
                disabled={loading || !senderEmail || !recipientEmail}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 
                  hover:from-blue-500 hover:to-purple-500 disabled:opacity-50 
                  disabled:cursor-not-allowed text-white font-semibold py-3 
                  rounded-lg transition transform hover:scale-105 active:scale-95"
            >
                {loading ? 'Initializing...' : 'Continue'}
            </button>
        </motion.div>
    );

    const renderOTPStep = () => (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
        >
            {/* Sender OTP */}
            <div className="bg-gradient-to-br from-blue-900/30 to-blue-800/20 
                      backdrop-blur-xl border border-blue-500/20 rounded-2xl p-6">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-blue-300">
                        Sender OTP Verification
                    </h3>
                    {otpVerification.sender?.verified ? (
                        <Check className="w-5 h-5 text-green-400" />
                    ) : (
                        <AlertCircle className="w-5 h-5 text-yellow-400" />
                    )}
                </div>

                <p className="text-gray-400 text-sm mb-4">
                    Email: <span className="text-blue-300">{senderEmail}</span>
                </p>

                <input
                    type="text"
                    maxLength="6"
                    value={senderOTP}
                    onChange={(e) => setSenderOTP(e.target.value.replace(/\D/g, ''))}
                    placeholder="000000"
                    className="w-full bg-gray-800/50 border border-gray-600/30 
                    rounded-lg px-4 py-3 text-2xl text-center font-mono 
                    text-white focus:outline-none focus:border-blue-500/50"
                />

                <button
                    onClick={() => handleVerifyOTP('sender')}
                    disabled={
                        loading || otpVerification.sender?.verified || senderOTP.length !== 6
                    }
                    className="w-full mt-4 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 
                    text-white font-semibold py-2 rounded-lg transition"
                >
                    {otpVerification.sender?.verified ? 'Verified ✓' : 'Verify Sender OTP'}
                </button>
            </div>

            {/* Recipient OTP */}
            <div className="bg-gradient-to-br from-purple-900/30 to-purple-800/20 
                      backdrop-blur-xl border border-purple-500/20 rounded-2xl p-6">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-purple-300">
                        Recipient OTP Verification
                    </h3>
                    {otpVerification.recipient?.verified ? (
                        <Check className="w-5 h-5 text-green-400" />
                    ) : (
                        <AlertCircle className="w-5 h-5 text-yellow-400" />
                    )}
                </div>

                <p className="text-gray-400 text-sm mb-4">
                    Email: <span className="text-purple-300">{recipientEmail}</span>
                </p>

                <input
                    type="text"
                    maxLength="6"
                    value={recipientOTP}
                    onChange={(e) => setRecipientOTP(e.target.value.replace(/\D/g, ''))}
                    placeholder="000000"
                    className="w-full bg-gray-800/50 border border-gray-600/30 
                    rounded-lg px-4 py-3 text-2xl text-center font-mono 
                    text-white focus:outline-none focus:border-purple-500/50"
                />

                <button
                    onClick={() => handleVerifyOTP('recipient')}
                    disabled={
                        loading
                        || otpVerification.recipient?.verified
                        || recipientOTP.length !== 6
                    }
                    className="w-full mt-4 bg-purple-600 hover:bg-purple-500 disabled:opacity-50 
                    text-white font-semibold py-2 rounded-lg transition"
                >
                    {otpVerification.recipient?.verified
                        ? 'Verified ✓'
                        : 'Verify Recipient OTP'}
                </button>
            </div>

            {/* Next Button */}
            {otpVerification.sender?.verified && otpVerification.recipient?.verified && (
                <button
                    onClick={() => setStep('file-selection')}
                    className="w-full bg-gradient-to-r from-green-600 to-emerald-600 
                    hover:from-green-500 hover:to-emerald-500 text-white 
                    font-semibold py-3 rounded-lg transition"
                >
                    Both Verified - Continue to File Upload
                </button>
            )}
        </motion.div>
    );

    const renderFileSelectionStep = () => (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
        >
            {/* File Upload */}
            <div
                onClick={() => fileInputRef.current?.click()}
                className="bg-gradient-to-br from-cyan-900/30 to-blue-900/30 
                  backdrop-blur-xl border-2 border-dashed border-cyan-500/30 
                  rounded-2xl p-8 text-center cursor-pointer hover:border-cyan-500/50 
                  transition group"
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    onChange={handleFileSelect}
                    className="hidden"
                />

                <Upload className="w-12 h-12 mx-auto text-cyan-400 mb-4 
                         group-hover:scale-110 transition" />

                <h3 className="text-xl font-semibold text-cyan-300 mb-2">
                    {selectedFile ? selectedFile.name : 'Click to select file'}
                </h3>

                <p className="text-gray-400 text-sm">
                    {selectedFile
                        ? `${(selectedFile.size / 1024 / 1024).toFixed(2)} MB`
                        : 'Supports: PDF, Images, Documents, Videos (Max 200MB)'}
                </p>

                {filePreview && (
                    <img
                        src={filePreview}
                        alt="Preview"
                        className="max-h-40 mx-auto mt-4 rounded-lg"
                    />
                )}
            </div>

            {/* Password */}
            {selectedFile && (
                <>
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                            <Lock className="w-4 h-4 inline mr-2 text-cyan-400" />
                            Encryption Password
                        </label>

                        <div className="relative">
                            <input
                                type={showPassword ? 'text' : 'password'}
                                value={encryptionPassword}
                                onChange={(e) => {
                                    setEncryptionPassword(e.target.value);
                                    setPasswordStrength(
                                        calculatePasswordStrength(e.target.value)
                                    );
                                }}
                                className="w-full bg-gray-800/50 border border-gray-600/30 
                          rounded-lg px-4 py-3 pr-12 text-white 
                          focus:outline-none focus:border-cyan-500/50 transition"
                                placeholder="Enter strong password"
                            />

                            <button
                                onClick={() => setShowPassword(!showPassword)}
                                className="absolute right-4 top-1/2 -translate-y-1/2 
                          text-gray-400 hover:text-gray-300"
                            >
                                {showPassword ? (
                                    <EyeOff className="w-5 h-5" />
                                ) : (
                                    <Eye className="w-5 h-5" />
                                )}
                            </button>
                        </div>

                        {/* Password Strength */}
                        {encryptionPassword && (
                            <div className="mt-3">
                                <div className="flex items-center justify-between text-xs mb-2">
                                    <span className="text-gray-400">Password Strength</span>
                                    <span className="text-cyan-300">{passwordStrength}%</span>
                                </div>
                                <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
                                    <motion.div
                                        initial={{ width: 0 }}
                                        animate={{ width: `${passwordStrength}%` }}
                                        className={`h-full ${getPasswordStrengthColor(passwordStrength)}`}
                                    />
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Upload Button */}
                    <button
                        onClick={handleUploadAndEncrypt}
                        disabled={
                            loading
                            || !encryptionPassword
                            || calculatePasswordStrength(encryptionPassword) < 50
                        }
                        className="w-full bg-gradient-to-r from-cyan-600 to-blue-600 
                      hover:from-cyan-500 hover:to-blue-500 disabled:opacity-50 
                      disabled:cursor-not-allowed text-white font-semibold py-3 
                      rounded-lg transition transform hover:scale-105 active:scale-95"
                    >
                        {loading ? 'Encrypting & Uploading...' : 'Encrypt & Upload'}
                    </button>
                </>
            )}
        </motion.div>
    );

    const renderSuccessStep = () => (
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-gradient-to-br from-green-900/30 to-emerald-900/30 
                 backdrop-blur-xl border border-green-500/20 rounded-2xl p-8 
                 text-center"
        >
            <div className="inline-block p-4 bg-green-500/20 rounded-full mb-4">
                <Check className="w-12 h-12 text-green-400" />
            </div>

            <h2 className="text-2xl font-bold text-green-300 mb-2">
                File Encrypted Successfully!
            </h2>

            <p className="text-gray-400 mb-6">
                The file has been encrypted and is ready to share
            </p>

            <div className="bg-gray-800/30 rounded-xl p-4 mb-6 text-left">
                <p className="text-sm text-gray-400 mb-2">Share ID:</p>
                <p className="font-mono text-cyan-300 break-all">{shareId}</p>

                <div className="grid grid-cols-2 gap-4 mt-6 text-sm">
                    <div>
                        <p className="text-gray-400">File</p>
                        <p className="text-white font-semibold">
                            {encryptedFileInfo?.filename}
                        </p>
                    </div>
                    <div>
                        <p className="text-gray-400">Size</p>
                        <p className="text-white font-semibold">
                            {(encryptedFileInfo?.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                    </div>
                </div>
            </div>

            <button
                onClick={() => {
                    navigator.clipboard.writeText(shareId);
                    toast.success('Share ID copied to clipboard');
                }}
                className="w-full bg-blue-600 hover:bg-blue-500 text-white 
                  font-semibold py-2 rounded-lg transition mb-4"
            >
                Copy Share ID
            </button>

            <button
                onClick={() => window.location.reload()}
                className="w-full bg-gray-700 hover:bg-gray-600 text-white 
                  font-semibold py-2 rounded-lg transition"
            >
                Encrypt Another File
            </button>
        </motion.div>
    );

    // =========================
    // MAIN RENDER
    // =========================

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900/20 
                    to-gray-900 p-6">
            <div className="max-w-2xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold text-transparent 
                        bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
                        Secure File Encryption
                    </h1>
                    <p className="text-gray-400 mt-2">
                        Industry-grade end-to-end encrypted file sharing
                    </p>
                </div>

                {/* Step Indicator */}
                <div className="flex items-center justify-center gap-4 mb-12">
                    {['intro', 'otp-verification', 'file-selection', 'success'].map(
                        (s, i) => (
                            <React.Fragment key={s}>
                                <div
                                    className={`w-10 h-10 rounded-full flex items-center justify-center 
                             font-semibold transition ${step === s
                                            ? 'bg-blue-600 text-white'
                                            : step > s
                                                ? 'bg-green-600 text-white'
                                                : 'bg-gray-700 text-gray-400'
                                        }`}
                                >
                                    {i + 1}
                                </div>
                                {i < 3 && (
                                    <div className={`h-1 w-12 transition ${step > s ? 'bg-green-600' : 'bg-gray-700'
                                        }`} />
                                )}
                            </React.Fragment>
                        )
                    )}
                </div>

                {/* Content */}
                {step === 'intro' && renderIntroStep()}
                {step === 'otp-verification' && renderOTPStep()}
                {step === 'file-selection' && renderFileSelectionStep()}
                {step === 'success' && renderSuccessStep()}
            </div>
        </div>
    );
};

export default SecureFileEncryption;
