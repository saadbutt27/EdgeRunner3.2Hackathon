import dynamic from 'next/dynamic';

// Dynamically import CameraCapture as a Client Component
const CameraCapture = dynamic(() => import('../components/CameraCapture'), { ssr: false });


export default function Home() {
  return (
    <div className='flex flex-col justify-center items-center pb-10'>
      <h1 className="bg-black text-white text-3xl font-bold p-5 mb-5 w-full text-center">X-ray Report Generator</h1>
      <CameraCapture />
    </div>
  );
}
