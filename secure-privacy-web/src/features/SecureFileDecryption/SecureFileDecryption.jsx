import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Download, Mail, Lock, Eye, EyeOff, Check, X, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import { useAuth } from '../../context/AuthContext';

/**
 * Secure File Decryption Component
 * Industry-grade decryption with OTP verification and file integrity
 */

const SecureFileDecryption = () => {
    // =========================
    // STATE MANAGEMENT
    // =========================

    const [step, setStep] = useState('share-id-input');

    // Step 1: Share ID
    const [shareId, setShareId] = useState('');
    const [shareInfo, setShareInfo] = useState(null);

    // Step 2: Recipient Email
    const [recipientEmail, setRecipientEmail] = useState('');

    // Step 3: OTP Verification
    const [otpSessionId, setOtpSessionId] = useState('');
    const [otpCode, setOtpCode] = useState('');
    const [otpVerified, setOtpVerified] = useState(false);
    const [decryptionToken, setDecryptionToken] = useState('');

    // Step 4: Decryption Password
    const [decryptionPassword, setDecryptionPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);

    // Loading & Status
    const [loading, setLoading] = useState(false);
    const [downloadProgress, setDownloadProgress] = useState(0);

    // Success
    const [decryptedFile, setDecryptedFile] = useState(null);
    const [fileMetadata, setFileMetadata] = useState(null);

    // =========================
    // UTILITY FUNCTIONS
    // =========================

    const validateEmail = (email) => {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    };

    const downloadFile = (data, filename, mimeType) => {
        const blob = new Blob([data], { type: mimeType });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);
    };

    // =========================
    // API CALLS
    // =========================

    const handleGetShareInfo = async () => {
        try {
            if (!shareId.trim()) {
                toast.error('Please enter a share ID');
                return;
            }

            setLoading(true);

            const response = await fetch(
                `http://localhost:8000/api/secure-share/share/${shareId}/info`
            );

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Share not found');
            }

            const data = await response.json();
            setShareInfo(data.share);

            toast.success('Share found. Enter recipient email to proceed.');
            setStep('recipient-email');

        } catch (error) {
            toast.error(error.message || 'Failed to fetch share info');
        } finally {
            setLoading(false);
        }
    };

    const handleRequestDecryption = async () => {
        try {
            if (!validateEmail(recipientEmail)) {
                toast.error('Invalid email address');
                return;
            }

            if (recipientEmail !== shareInfo?.recipient_email) {
                toast.error('You are not the authorized recipient');
                return;
            }

            setLoading(true);

            const response = await fetch(
                'http://localhost:8000/api/secure-share/decrypt/request',
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        share_id: shareId,
                        recipient_email: recipientEmail
                    })
                }
            );

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to request decryption');
            }

            const data = await response.json();

            setOtpSessionId(data.session_id);

            toast.success('OTP sent to your email. Check your inbox.');

            setStep('otp-verification');

        } catch (error) {
            toast.error(error.message || 'Failed to request decryption');
        } finally {
            setLoading(false);
        }
    };

    const handleVerifyOTP = async () => {
        try {
            if (!otpCode || otpCode.length !== 6) {
                toast.error('Please enter valid 6-digit OTP');
                return;
            }

            setLoading(true);

            const response = await fetch(
                'http://localhost:8000/api/secure-share/decrypt/verify-otp',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'recipient-email': recipientEmail
                    },
                    body: JSON.stringify({
                        session_id: otpSessionId,
                        otp_code: otpCode
                    })
                }
            );

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'OTP verification failed');
            }

            const data = await response.json();

            setDecryptionToken(data.access_token);
            setOtpVerified(true);

            toast.success('OTP verified successfully');

            setStep('password-entry');

        } catch (error) {
            toast.error(error.message || 'OTP verification failed');
        } finally {
            setLoading(false);
        }
    };

    const handleDecryptFile = async () => {
        try {
            if (!decryptionPassword) {
                toast.error('Please enter decryption password');
                return;
            }

            setLoading(true);
            setDownloadProgress(0);

            const response = await fetch(
                'http://localhost:8000/api/secure-share/decrypt/download',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'recipient-email': recipientEmail,
                        'authorization': `Bearer ${decryptionToken}`
                    },
                    body: JSON.stringify({
                        share_id: shareId,
                        password: decryptionPassword
                    })
                }
            );

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Decryption failed');
            }

            const data = await response.json();

            if (!data.success) {
                throw new Error(data.message || 'Decryption failed');
            }

            // Convert base64 to bytes if needed
            let fileData = data.file_data;

            if (typeof fileData === 'string') {
                const binaryString = atob(fileData);
                const bytes = new Uint8Array(binaryString.length);
                for (let i = 0; i < binaryString.length; i++) {
                    bytes[i] = binaryString.charCodeAt(i);
                }
                fileData = bytes;
            }

            setDecryptedFile(fileData);
            setFileMetadata(data.metadata);

            toast.success('File decrypted successfully!');

            setStep('success');

        } catch (error) {
            toast.error(error.message || 'File decryption failed');
        } finally {
            setLoading(false);
            setDownloadProgress(0);
        }
    };

    // =========================
    // RENDER METHODS
    // =========================

    const renderShareIdInputStep = () => (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gradient-to-br from-indigo-900/30 to-purple-900/30 
                 backdrop-blur-xl border border-indigo-500/20 rounded-2xl p-8"
        >
            <div className="text-center mb-8">
                <div className="inline-block p-4 bg-indigo-500/20 rounded-xl mb-4">
                    <Download className="w-8 h-8 text-indigo-400" />
                </div>
                <h2 className="text-3xl font-bold text-transparent 
                      bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">
                    Decrypt Shared File
                </h2>
                <p className="text-gray-400 mt-2">
                    Enter the share ID provided by the sender
                </p>
            </div>

            <div className="mb-6">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                    Share ID
                </label>
                <input
                    type="text"
                    value={shareId}
                    onChange={(e) => setShareId(e.target.value)}
                    placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                    className="w-full bg-gray-800/50 border border-gray-600/30 
                    rounded-lg px-4 py-3 text-white focus:outline-none 
                    focus:border-indigo-500/50 transition font-mono"
                />
                <p className="text-xs text-gray-500 mt-2">
                    You can paste the share ID from the sender
                </p>
            </div>

            <button
                onClick={handleGetShareInfo}
                disabled={loading || !shareId.trim()}
                className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 
                  hover:from-indigo-500 hover:to-purple-500 disabled:opacity-50 
                  disabled:cursor-not-allowed text-white font-semibold py-3 
                  rounded-lg transition transform hover:scale-105 active:scale-95"
            >
                {loading ? 'Verifying...' : 'Verify Share ID'}
            </button>
        </motion.div>
    );

    const renderRecipientEmailStep = () => (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
        >
            {/* Share Info */}
            <div className="bg-gradient-to-br from-blue-900/30 to-indigo-900/30 
                      backdrop-blur-xl border border-blue-500/20 rounded-2xl p-6">
                <h3 className="text-lg font-semibold text-blue-300 mb-4">
                    File Details
                </h3>

                <div className="space-y-3 text-sm">
                    <div className="flex justify-between">
                        <span className="text-gray-400">Filename:</span>
                        <span className="text-white font-semibold">
                            {shareInfo?.filename}
                        </span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-gray-400">Size:</span>
                        <span className="text-white font-semibold">
                            {(shareInfo?.size / 1024 / 1024).toFixed(2)} MB
                        </span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-gray-400">From:</span>
                        <span className="text-white font-semibold">
                            {shareInfo?.sender_email}
                        </span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-gray-400">For:</span>
                        <span className="text-white font-semibold">
                            {shareInfo?.recipient_email}
                        </span>
                    </div>
                </div>
            </div>

            {/* Recipient Email */}
            <div className="bg-gradient-to-br from-purple-900/30 to-indigo-900/30 
                      backdrop-blur-xl border border-purple-500/20 rounded-2xl p-6">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                    <Mail className="w-4 h-4 inline mr-2 text-purple-400" />
                    Your Email Address
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

                <p className="text-xs text-gray-500 mt-3">
                    Must match the recipient email from the share
                </p>

                <button
                    onClick={handleRequestDecryption}
                    disabled={loading || !recipientEmail}
                    className="w-full mt-4 bg-gradient-to-r from-purple-600 to-indigo-600 
                    hover:from-purple-500 hover:to-indigo-500 disabled:opacity-50 
                    text-white font-semibold py-3 rounded-lg transition"
                >
                    {loading ? 'Sending OTP...' : 'Request Decryption Access'}
                </button>
            </div>
        </motion.div>
    );

    const renderOTPVerificationStep = () => (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gradient-to-br from-yellow-900/30 to-orange-900/30 
                 backdrop-blur-xl border border-yellow-500/20 rounded-2xl p-8"
        >
            <div className="text-center mb-8">
                <AlertCircle className="w-12 h-12 text-yellow-400 mx-auto mb-4" />
                <h2 className="text-2xl font-semibold text-yellow-300">
                    Verify Your Identity
                </h2>
                <p className="text-gray-400 mt-2">
                    Enter the 6-digit OTP sent to {recipientEmail}
                </p>
            </div>

            <div className="mb-6">
                <input
                    type="text"
                    maxLength="6"
                    value={otpCode}
                    onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, ''))}
                    placeholder="000000"
                    className="w-full bg-gray-800/50 border border-gray-600/30 
                    rounded-lg px-4 py-6 text-4xl text-center font-mono 
                    text-yellow-300 focus:outline-none focus:border-yellow-500/50"
                />

                <p className="text-xs text-gray-500 mt-3 text-center">
                    OTP expires in 10 minutes
                </p>
            </div>

            <button
                onClick={handleVerifyOTP}
                disabled={loading || otpCode.length !== 6}
                className="w-full bg-gradient-to-r from-yellow-600 to-orange-600 
                  hover:from-yellow-500 hover:to-orange-500 disabled:opacity-50 
                  text-white font-semibold py-3 rounded-lg transition"
            >
                {loading ? 'Verifying OTP...' : 'Verify OTP'}
            </button>
        </motion.div>
    );

    const renderPasswordEntryStep = () => (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gradient-to-br from-cyan-900/30 to-blue-900/30 
                 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-8"
        >
            <div className="text-center mb-8">
                <div className="inline-block p-4 bg-cyan-500/20 rounded-xl mb-4">
                    <Lock className="w-8 h-8 text-cyan-400" />
                </div>
                <h2 className="text-2xl font-semibold text-cyan-300">
                    Enter Decryption Password
                </h2>
                <p className="text-gray-400 mt-2">
                    Provided by the sender
                </p>
            </div>

            <div className="mb-6">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                    Decryption Password
                </label>

                <div className="relative">
                    <input
                        type={showPassword ? 'text' : 'password'}
                        value={decryptionPassword}
                        onChange={(e) => setDecryptionPassword(e.target.value)}
                        className="w-full bg-gray-800/50 border border-gray-600/30 
                      rounded-lg px-4 py-3 pr-12 text-white 
                      focus:outline-none focus:border-cyan-500/50 transition"
                        placeholder="Enter password"
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
            </div>

            <button
                onClick={handleDecryptFile}
                disabled={loading || !decryptionPassword}
                className="w-full bg-gradient-to-r from-cyan-600 to-blue-600 
                  hover:from-cyan-500 hover:to-blue-500 disabled:opacity-50 
                  text-white font-semibold py-3 rounded-lg transition"
            >
                {loading ? 'Decrypting & Downloading...' : 'Decrypt & Download File'}
            </button>

            {downloadProgress > 0 && downloadProgress < 100 && (
                <div className="mt-4">
                    <div className="flex justify-between text-xs mb-2">
                        <span className="text-gray-400">Progress</span>
                        <span className="text-cyan-300">{downloadProgress}%</span>
                    </div>
                    <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
                        <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${downloadProgress}%` }}
                            className="h-full bg-gradient-to-r from-cyan-500 to-blue-500"
                        />
                    </div>
                </div>
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
                File Decrypted Successfully!
            </h2>

            <p className="text-gray-400 mb-8">
                Your decrypted file is ready to download
            </p>

            <div className="bg-gray-800/30 rounded-xl p-6 mb-8 text-left">
                <h3 className="text-sm font-semibold text-gray-300 mb-4">
                    File Information
                </h3>

                <div className="space-y-3 text-sm">
                    <div className="flex justify-between">
                        <span className="text-gray-400">Filename:</span>
                        <span className="text-white font-semibold">
                            {fileMetadata?.filename}
                        </span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-gray-400">Size:</span>
                        <span className="text-white font-semibold">
                            {(fileMetadata?.file_size / 1024 / 1024).toFixed(2)} MB
                        </span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-gray-400">Type:</span>
                        <span className="text-white font-semibold">
                            {fileMetadata?.mime_type}
                        </span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-gray-400">Checksum (SHA-256):</span>
                        <span className="text-cyan-300 font-mono text-xs truncate">
                            {fileMetadata?.checksum}
                        </span>
                    </div>
                </div>
            </div>

            <button
                onClick={() => {
                    downloadFile(
                        decryptedFile,
                        fileMetadata?.filename,
                        fileMetadata?.mime_type
                    );
                }}
                className="w-full bg-gradient-to-r from-green-600 to-emerald-600 
                  hover:from-green-500 hover:to-emerald-500 text-white 
                  font-semibold py-3 rounded-lg transition mb-4 
                  flex items-center justify-center gap-2"
            >
                <Download className="w-5 h-5" />
                Download File
            </button>

            <button
                onClick={() => window.location.reload()}
                className="w-full bg-gray-700 hover:bg-gray-600 text-white 
                  font-semibold py-2 rounded-lg transition"
            >
                Decrypt Another File
            </button>
        </motion.div>
    );

    // =========================
    // MAIN RENDER
    // =========================

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-indigo-900/20 
                    to-gray-900 p-6">
            <div className="max-w-2xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold text-transparent 
                        bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">
                        Decrypt Shared File
                    </h1>
                    <p className="text-gray-400 mt-2">
                        Securely decrypt encrypted files shared with you
                    </p>
                </div>

                {/* Step Indicator */}
                <div className="flex items-center justify-center gap-2 mb-12 text-xs 
                       overflow-x-auto pb-2">
                    {[
                        { id: 'share-id-input', label: '1' },
                        { id: 'recipient-email', label: '2' },
                        { id: 'otp-verification', label: '3' },
                        { id: 'password-entry', label: '4' },
                        { id: 'success', label: '✓' }
                    ].map((s, i) => (
                        <React.Fragment key={s.id}>
                            <div
                                className={`w-10 h-10 rounded-full flex items-center justify-center 
                           font-semibold transition whitespace-nowrap ${step === s.id
                                        ? 'bg-indigo-600 text-white'
                                        : ['share-id-input', 'recipient-email', 'otp-verification',
                                            'password-entry', 'success'].indexOf(step)
                                            > ['share-id-input', 'recipient-email', 'otp-verification',
                                                'password-entry', 'success'].indexOf(s.id)
                                            ? 'bg-green-600 text-white'
                                            : 'bg-gray-700 text-gray-400'
                                    }`}
                            >
                                {s.label}
                            </div>
                            {i < 4 && (
                                <div className={`h-1 w-6 transition ${['share-id-input', 'recipient-email', 'otp-verification',
                                    'password-entry', 'success'].indexOf(step)
                                    > ['share-id-input', 'recipient-email', 'otp-verification',
                                        'password-entry', 'success'].indexOf(s.id)
                                    ? 'bg-green-600'
                                    : 'bg-gray-700'
                                    }`} />
                            )}
                        </React.Fragment>
                    ))}
                </div>

                {/* Content */}
                {step === 'share-id-input' && renderShareIdInputStep()}
                {step === 'recipient-email' && renderRecipientEmailStep()}
                {step === 'otp-verification' && renderOTPVerificationStep()}
                {step === 'password-entry' && renderPasswordEntryStep()}
                {step === 'success' && renderSuccessStep()}
            </div>
        </div>
    );
};

export default SecureFileDecryption;
