"use client"
import React, { useEffect, useRef, useState } from 'react';
import { Button } from './ui/button';
import { Label } from './ui/label';
import { Input } from './ui/input';

const CameraCapture: React.FC = () => {
    const videoRef = useRef<HTMLVideoElement>(null);
    const streamRef = useRef<MediaStream | null>(null);
    const [capturedImage, setCapturedImage] = useState<string | null>(null);
    const [isCameraOn, setIsCameraOn] = useState(false); // Track camera state
    const [isImageSubmitted, setIsImageSubmitted] = useState(false); // To track image submission
    const [patientName, setPatientName] = useState<string>(''); // New state for patient name
    const [patientDOB, setPatientDOB] = useState<string>(''); // New state for patient DOB
    const [pdfUrl, setPdfUrl] = useState<string | null>(null); // State to store the PDF URL

     // useEffect to check if videoRef is set properly after rendering
    useEffect(() => {
        if (isCameraOn && videoRef.current) {
            // Start camera if it's not already running and video element exists
            startCamera();
        }
    }, [isCameraOn]);

  // Start the camera
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      streamRef.current = stream;
      if (videoRef.current) {
          videoRef.current.srcObject = stream;
        } else {
            console.error("Video element not available");
        }
        setIsCameraOn(true); // Update state to indicate camera is on
    } catch (error) {
      console.error("Error accessing the camera: ", error);
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      // Stop all the media tracks (audio and video)
      streamRef.current.getTracks().forEach((track) => {
        track.stop(); // Stop each track explicitly
      });
      
      // Release the camera by setting the streamRef to null
      streamRef.current = null;
    }
  
    if (videoRef.current) {
      videoRef.current.srcObject = null; // Clear the video source
    }
  
    setIsCameraOn(false); // Update state
    // console.log("Camera stopped, state updated");
  };
  

    // Capture image from the video and stop the camera after capturing
    const captureImage = () => {
        if (videoRef.current && videoRef.current.srcObject && canvasRef.current) {
        const canvas = canvasRef.current;
        const video = videoRef.current;
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');
        if (context) {
          context.drawImage(video, 0, 0, canvas.width, canvas.height);
          const imageUrl = canvas.toDataURL('image/png');
          setCapturedImage(imageUrl);
          
          // Stop the camera after capturing the image
          stopCamera();
        }
      }
    };

  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Handle image file upload and convert it to base64
  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
        const reader = new FileReader();
        reader.onloadend = () => {
            setCapturedImage(reader.result as string); // Base64 URL
        };
        reader.readAsDataURL(file); // Convert uploaded image to base64
    }
  };

  // Handle form submission
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!capturedImage || !patientName || !patientDOB) {
      console.log("All fields are required.");
      return;
    }

    try {
      console.log(patientName, patientDOB)
      const response = await fetch("/api/py/image", {
          method: "POST",
          body: JSON.stringify({
            image: capturedImage,
            patient_name: patientName,
            patient_dob: patientDOB,
          }),
          headers: {
            "Content-Type": "application/json",
          },
      });

      if (response.ok) {
        const blob = await response.blob(); // Get the PDF as a blob
        const pdfUrl = URL.createObjectURL(blob); // Create a URL for the PDF
        setPdfUrl(pdfUrl); // Store the PDF URL in state
        setIsImageSubmitted(true);
      } else {
          console.error("Error submitting image:", response.statusText);
      }
    } catch (error) {
        console.error("Error submitting image:", error);
    } finally {
      // Reset the captured image after submission
      setCapturedImage(null);
    }
  };

  useEffect(() => {
    if (capturedImage && window.innerWidth < 768) {
      window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
    }
  }, [capturedImage]);

  return (
    <div className="container mx-auto p-10">
      <div className="flex flex-col lg:flex-row lg:items-start gap-8 border-2 p-4 h-full rounded-md shadow">
        {/* Left section for camera and upload controls */}
        <div className="flex flex-col items-center justify-center gap-4 lg:w-1/2">
          {/* Camera controls */}
          <div className="flex justify-start items-center gap-4">
              {!isCameraOn ? (
                  <Button onClick={startCamera}>Start Camera</Button>
              ) : (
                  <Button onClick={stopCamera}>Stop Camera</Button>
              )} 
          </div>

          {/* Video stream when the camera is on */}
          {isCameraOn && (
            <div className="flex flex-col items-center gap-4 mt-5">
                <video 
                  className="border-2 border-black" 
                  ref={videoRef} 
                  autoPlay
                  playsInline 
                  width="100%" 
                />
                <Button onClick={captureImage} disabled={!isCameraOn}>
                    Capture Image
                </Button>
            </div>
          )}

          <p className='font-bold text-xl'>OR</p>

          {/* Image upload */}
          <div className="grid w-full max-w-sm items-center gap-1.5">
              <Label htmlFor="upload-image" className="text-lg font-bold text-center mb-2">
                  Upload Image:
              </Label>
              <Input 
                type="file" 
                id="upload-image" 
                accept="image/*" 
                onChange={handleImageUpload} 
              />
          </div>
        </div>


        {/* Right section for displaying the captured/uploaded image */}
        {capturedImage && (
            <div className="lg:w-1/2 flex flex-col justify-center items-center gap-y-4 mt-10 lg:mt-0">
              <h3 className="text-xl font-bold">Preview Image:</h3>
              <img src={capturedImage} alt="Captured or Uploaded" height={500} width={300}/>
              {/* New input fields for patient name and DOB */}
              <div className="flex gap-x-3">
                <div className="mt-4">
                  <Label htmlFor="patient-name" className="text-sm font-bold">Patient's Name:</Label>
                  <Input
                    type="text"
                    id="patient-name"
                    value={patientName}
                    onChange={(e) => setPatientName(e.target.value)}
                    placeholder="Enter patient's name"
                    className="mt-2"
                    required
                  />
                </div>
                <div className="mt-4">
                  <Label htmlFor="patient-dob" className="text-sm font-bold">Date of Birth:</Label>
                  <Input
                    type="date"
                    id="patient-dob"
                    value={patientDOB}
                    onChange={(e) => setPatientDOB(e.target.value)}
                    className="mt-2"
                    required
                  />
                </div>
              </div>
              <Button onClick={handleSubmit}>Submit Image</Button>
            </div>
        )}

        {/* Right div for image submission status and PDF */}
        {isImageSubmitted && pdfUrl && (
          <div className="md:w-1/2 flex flex-col items-center gap-y-3">
            <p className="text-green-500 font-bold">Image submitted successfully! You may download you report.</p>
            <iframe
              src={pdfUrl}
              className="border border-gray-300"
              width="100%"
              height="400px"
              title="Report PDF"
            ></iframe>
            <Button>
              <a href={pdfUrl} download="report.pdf">
                Download Report
              </a>
            </Button>
          </div>
        )}
      </div>
      {/* Hidden canvas for image capture */}
      <canvas ref={canvasRef} style={{ display: "none" }} />
    </div>
  );
};

export default CameraCapture;
