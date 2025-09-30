import React, { useRef, useEffect, useState, Suspense } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sphere, Box, Text } from '@react-three/drei';
import * as THREE from 'three';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { 
  Heart, 
  Shield, 
  Brain, 
  Activity, 
  MessageCircle, 
  X, 
  Moon, 
  Sun,
  Stethoscope,
  Zap,
  Users,
  Award,
  Github,
  Twitter,
  Linkedin,
  Mail
} from 'lucide-react';
import Chatbot from './components/Chatbot.jsx';

// Register GSAP plugins
gsap.registerPlugin(ScrollTrigger);

// 3D Medical Globe Component
const MedicalGlobe = () => {
  const meshRef = useRef();
  const particlesRef = useRef();
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.005;
      meshRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.5) * 0.1;
    }
    
    if (particlesRef.current) {
      particlesRef.current.rotation.y -= 0.002;
    }
  });

  // Create particles
  const particles = [];
  for (let i = 0; i < 100; i++) {
    const phi = Math.acos(-1 + (2 * i) / 100);
    const theta = Math.sqrt(100 * Math.PI) * phi;
    
    particles.push(
      <mesh
        key={i}
        position={[
          2 * Math.cos(theta) * Math.sin(phi),
          2 * Math.sin(theta) * Math.sin(phi),
          2 * Math.cos(phi)
        ]}
      >
        <sphereGeometry args={[0.02, 8, 8]} />
        <meshBasicMaterial color="#1e90ff" />
      </mesh>
    );
  }

  return (
    <group>
      <mesh ref={meshRef}>
        <sphereGeometry args={[1.5, 32, 32]} />
        <meshStandardMaterial 
          color="#1e90ff" 
          wireframe 
          transparent 
          opacity={0.6} 
        />
      </mesh>
      <group ref={particlesRef}>
        {particles}
      </group>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} intensity={1} />
    </group>
  );
};

// Floating Medical Icons Component
const FloatingIcons = () => {
  const icons = [
    { icon: Heart, position: [-3, 2, 0], color: '#ff6b6b' },
    { icon: Shield, position: [3, -1, 0], color: '#4ecdc4' },
    { icon: Brain, position: [-2, -2, 1], color: '#45b7d1' },
    { icon: Activity, position: [2, 2, -1], color: '#96ceb4' },
  ];

  return (
    <group>
      {icons.map((item, index) => (
        <Text
          key={index}
          position={item.position}
          fontSize={0.5}
          color={item.color}
          anchorX="center"
          anchorY="middle"
        >
          ❤️
        </Text>
      ))}
    </group>
  );
};

// Hero Section Component
const Hero = ({ onChatOpen, darkMode }) => {
  const heroRef = useRef();
  
  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.hero-title', 
        { y: 100, opacity: 0 },
        { y: 0, opacity: 1, duration: 1.5, ease: 'power3.out' }
      );
      
      gsap.fromTo('.hero-subtitle', 
        { y: 50, opacity: 0 },
        { y: 0, opacity: 1, duration: 1.2, delay: 0.3, ease: 'power3.out' }
      );
      
      gsap.fromTo('.hero-cta', 
        { scale: 0, opacity: 0 },
        { scale: 1, opacity: 1, duration: 0.8, delay: 0.8, ease: 'back.out(1.7)' }
      );

      gsap.fromTo('.hero-3d', 
        { scale: 0, rotationY: 180 },
        { scale: 1, rotationY: 0, duration: 2, delay: 0.5, ease: 'power3.out' }
      );
    }, heroRef);

    return () => ctx.revert();
  }, []);

  return (
    <section 
      ref={heroRef}
      className={`relative min-h-screen flex items-center justify-center overflow-hidden ${
        darkMode ? 'bg-gray-900' : 'bg-gradient-to-br from-blue-50 to-indigo-100'
      }`}
    >
      {/* Animated Background */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-10 left-10 w-20 h-20 bg-blue-500 rounded-full animate-pulse"></div>
        <div className="absolute top-40 right-20 w-16 h-16 bg-green-500 rounded-full animate-bounce"></div>
        <div className="absolute bottom-20 left-20 w-12 h-12 bg-purple-500 rounded-full animate-ping"></div>
        <div className="absolute bottom-40 right-40 w-24 h-24 bg-pink-500 rounded-full animate-pulse"></div>
      </div>

      <div className="container mx-auto px-4 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        {/* Left Content */}
        <div className="text-center lg:text-left z-10">
          <h1 className={`hero-title text-5xl lg:text-7xl font-bold mb-6 ${
            darkMode ? 'text-white' : 'text-gray-900'
          }`}>
            FALCON
            <span className="text-blue-500">CARE</span>
          </h1>
          
          <p className={`hero-subtitle text-xl lg:text-2xl mb-8 ${
            darkMode ? 'text-gray-300' : 'text-gray-700'
          }`}>
            Revolutionary AI-powered healthcare assistance at your fingertips
          </p>
          
          <button
            onClick={onChatOpen}
            className="hero-cta bg-blue-500 hover:bg-blue-600 text-white px-8 py-4 rounded-full text-lg font-semibold shadow-2xl transform hover:scale-105 transition-all duration-300 flex items-center justify-center mx-auto lg:mx-0 gap-3"
          >
            <MessageCircle className="w-6 h-6" />
            Chat with FALCONCARE
          </button>
        </div>

        {/* Right 3D Animation */}
        <div className="hero-3d h-96 lg:h-[500px]">
          <Canvas camera={{ position: [0, 0, 5] }}>
            <Suspense fallback={null}>
              <MedicalGlobe />
              <FloatingIcons />
              <OrbitControls enableZoom={false} enablePan={false} autoRotate />
            </Suspense>
          </Canvas>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div className={`w-6 h-10 border-2 rounded-full flex justify-center ${
          darkMode ? 'border-white' : 'border-gray-900'
        }`}>
          <div className={`w-1 h-3 rounded-full mt-2 animate-pulse ${
            darkMode ? 'bg-white' : 'bg-gray-900'
          }`}></div>
        </div>
      </div>
    </section>
  );
};

// Features Section Component
const Features = ({ darkMode }) => {
  const featuresRef = useRef();
  
  const features = [
    {
      icon: Heart,
      title: "Heart Health Monitoring",
      description: "Real-time cardiovascular health assessment with AI-powered insights",
      color: "text-red-500"
    },
    {
      icon: Brain,
      title: "Mental Health Support",
      description: "Comprehensive mental wellness guidance and stress management",
      color: "text-purple-500"
    },
    {
      icon: Shield,
      title: "Preventive Care",
      description: "Proactive health recommendations to prevent illness before it starts",
      color: "text-green-500"
    },
    {
      icon: Activity,
      title: "Fitness Tracking",
      description: "Personalized workout plans and activity monitoring",
      color: "text-blue-500"
    },
    {
      icon: Stethoscope,
      title: "Symptom Analysis",
      description: "Advanced symptom checker with medical database integration",
      color: "text-indigo-500"
    },
    {
      icon: Zap,
      title: "Emergency Response",
      description: "Quick emergency protocols and nearest healthcare facility finder",
      color: "text-yellow-500"
    }
  ];

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.features-title',
        { y: 50, opacity: 0 },
        {
          y: 0, 
          opacity: 1, 
          duration: 1,
          scrollTrigger: {
            trigger: '.features-title',
            start: 'top 80%',
          }
        }
      );

      gsap.fromTo('.feature-card',
        { y: 100, opacity: 0, scale: 0.8 },
        {
          y: 0,
          opacity: 1,
          scale: 1,
          duration: 0.8,
          stagger: 0.2,
          ease: 'back.out(1.7)',
          scrollTrigger: {
            trigger: '.features-grid',
            start: 'top 80%',
          }
        }
      );
    }, featuresRef);

    return () => ctx.revert();
  }, []);

  return (
    <section 
      ref={featuresRef}
      className={`py-20 ${
        darkMode ? 'bg-gray-800' : 'bg-white'
      }`}
    >
      <div className="container mx-auto px-4">
        <h2 className={`features-title text-4xl lg:text-5xl font-bold text-center mb-16 ${
          darkMode ? 'text-white' : 'text-gray-900'
        }`}>
          Revolutionary Healthcare Features
        </h2>
        
        <div className="features-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className={`feature-card p-8 rounded-2xl shadow-xl hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 group cursor-pointer ${
                darkMode ? 'bg-gray-700 hover:bg-gray-600' : 'bg-white hover:bg-gray-50'
              }`}
            >
              <div className={`${feature.color} mb-6 transform group-hover:scale-110 transition-transform duration-300`}>
                <feature.icon className="w-12 h-12" />
              </div>
              
              <h3 className={`text-2xl font-bold mb-4 ${
                darkMode ? 'text-white' : 'text-gray-900'
              }`}>
                {feature.title}
              </h3>
              
              <p className={`text-lg ${
                darkMode ? 'text-gray-300' : 'text-gray-600'
              }`}>
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

// Statistics Section
const Statistics = ({ darkMode }) => {
  const statsRef = useRef();
  
  const stats = [
    { number: '50K+', label: 'Users Helped', icon: Users },
    { number: '99%', label: 'Accuracy Rate', icon: Award },
    { number: '24/7', label: 'Available', icon: Activity },
    { number: '100+', label: 'Health Conditions', icon: Heart },
  ];

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.stat-item',
        { y: 50, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 1,
          stagger: 0.2,
          scrollTrigger: {
            trigger: '.stats-container',
            start: 'top 80%',
          }
        }
      );
    }, statsRef);

    return () => ctx.revert();
  }, []);

  return (
    <section 
      ref={statsRef}
      className={`py-20 ${
        darkMode ? 'bg-gray-900' : 'bg-gradient-to-r from-blue-500 to-purple-600'
      }`}
    >
      <div className="container mx-auto px-4">
        <div className="stats-container grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <div key={index} className="stat-item text-center text-white">
              <div className="mb-4 flex justify-center">
                <stat.icon className="w-12 h-12 text-white" />
              </div>
              <div className="text-4xl lg:text-5xl font-bold mb-2">{stat.number}</div>
              <div className="text-xl opacity-90">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

// Footer Component
const Footer = ({ darkMode }) => {
  const footerRef = useRef();
  
  const socialLinks = [
    { icon: Github, href: '#', label: 'GitHub' },
    { icon: Twitter, href: '#', label: 'Twitter' },
    { icon: Linkedin, href: '#', label: 'LinkedIn' },
    { icon: Mail, href: '#', label: 'Email' },
  ];

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.footer-content',
        { y: 50, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 1,
          scrollTrigger: {
            trigger: '.footer-content',
            start: 'top 90%',
          }
        }
      );
    }, footerRef);

    return () => ctx.revert();
  }, []);

  return (
    <footer 
      ref={footerRef}
      className={`py-12 ${
        darkMode ? 'bg-gray-900 border-t border-gray-800' : 'bg-gray-900'
      }`}
    >
      <div className="container mx-auto px-4">
        <div className="footer-content text-center">
          <h3 className="text-3xl font-bold text-white mb-4">FALCONCARE</h3>
          <p className="text-gray-400 mb-8 max-w-md mx-auto">
            Revolutionizing healthcare with AI-powered assistance for a healthier tomorrow
          </p>
          
          <div className="flex justify-center space-x-6 mb-8">
            {socialLinks.map((link, index) => (
              <a
                key={index}
                href={link.href}
                aria-label={link.label}
                className="text-gray-400 hover:text-white transform hover:scale-110 transition-all duration-300"
              >
                <link.icon className="w-6 h-6" />
              </a>
            ))}
          </div>
          
          <div className="border-t border-gray-800 pt-8">
            <p className="text-gray-500">
              © 2024 FALCONCARE. All rights reserved. Built for healthcare innovation.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

// Main App Component
const App = () => {
  const [chatOpen, setChatOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    // Initialize GSAP
    gsap.registerPlugin(ScrollTrigger);
    
    // Smooth scrolling
    const lenis = {
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t))
    };

    return () => {
      ScrollTrigger.getAll().forEach(t => t.kill());
    };
  }, []);

  return (
    <div className={`min-h-screen ${darkMode ? 'dark' : ''}`}>
      {/* Dark Mode Toggle */}
      <button
        onClick={() => setDarkMode(!darkMode)}
        className="fixed top-6 right-6 z-40 p-3 rounded-full bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transform hover:scale-110 transition-all duration-300"
      >
        {darkMode ? <Sun className="w-6 h-6 text-yellow-500" /> : <Moon className="w-6 h-6 text-gray-700" />}
      </button>

      {/* Floating Chat Button */}
      {!chatOpen && (
        <button
          onClick={() => setChatOpen(true)}
          className="fixed bottom-6 right-6 z-40 bg-blue-500 hover:bg-blue-600 text-white p-4 rounded-full shadow-2xl transform hover:scale-110 transition-all duration-300 animate-pulse"
        >
          <MessageCircle className="w-8 h-8" />
        </button>
      )}

      {/* Main Content */}
      <Hero onChatOpen={() => setChatOpen(true)} darkMode={darkMode} />
      <Features darkMode={darkMode} />
      <Statistics darkMode={darkMode} />
      <Footer darkMode={darkMode} />

      {/* Chatbot */}
      <Chatbot 
        isOpen={chatOpen} 
        onClose={() => setChatOpen(false)} 
        darkMode={darkMode} 
      />
    </div>
  );
};

export default App;
