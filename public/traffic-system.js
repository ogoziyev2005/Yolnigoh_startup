// ======================
// Traffic Management System
// Module: trafficSystem.js
// Version: 1.0
// Author: Yo'lNigoh AI Team
// ======================

const TrafficSystem = (() => {
    // DOM Elements
    const elements = {
      videoFeed: document.getElementById('videoFeed'),
      loadingIndicator: document.getElementById('loadingIndicator'),
      vehicleCount: document.getElementById('vehicleCount'),
      trafficStatus: document.getElementById('trafficStatus'),
      carCount: document.getElementById('carCount'),
      busCount: document.getElementById('busCount'),
      truckCount: document.getElementById('truckCount'),
      motorcycleCount: document.getElementById('motorcycleCount'),
      redLight: document.getElementById('redLight'),
      yellowLight: document.getElementById('yellowLight'),
      greenLight: document.getElementById('greenLight'),
      lightTimer: document.getElementById('lightTimer'),
      locationStatus: document.getElementById('locationStatus'),
      navLinks: document.querySelectorAll('.nav-link'),
      pages: document.querySelectorAll('.page')
    };
  
    // Traffic light states
    const LIGHT_STATES = {
      RED: 'red',
      YELLOW: 'yellow',
      GREEN: 'green'
    };
  
    // Configuration
    const config = {
      updateIntervals: {
        video: 1000,    // Update video every 1 second
        data: 5000,     // Update traffic data every 5 seconds
        timer: 1000,    // Update traffic light timer every 1 second
        location: 5000  // Rotate location every 5 seconds
      },
      locations: [
        "Toshkent sh., Yunusobod t.",
        "Toshkent sh., Mirzo Ulug'bek t.",
        "Toshkent sh., Shayxontohur t.",
        "Samarqand sh., Registon ko'chasi",
        "Buxoro sh., Labi Hovuz"
      ]
    };
  
    // System state
    let state = {
      currentLightState: LIGHT_STATES.GREEN,
      timerValue: 15,
      currentGreenTime: 15,
      currentLocationIndex: 0,
      intervals: {}
    };
  
    // ======================
    // Page Navigation
    // ======================
    
    function initNavigation() {
      // Show home page by default
      showPage('home');
      
      // Add event listeners to nav links
      elements.navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
          e.preventDefault();
          showPage(link.dataset.page);
        });
      });
    }
    
    function showPage(pageId) {
      // Hide all pages
      elements.pages.forEach(page => page.classList.add('hidden'));
      
      // Show selected page
      document.getElementById(`${pageId}-page`).classList.remove('hidden');
      
      // Update active nav link
      elements.navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.dataset.page === pageId) {
          link.classList.add('active');
        }
      });
    }
  
    // ======================
    // Traffic Light Control
    // ======================
    
    function initTrafficLight() {
      updateTrafficLight(0); // Initialize with 0 vehicles
      state.intervals.timer = setInterval(updateTimer, config.updateIntervals.timer);
    }
    
    function updateTrafficLight(vehicleCount) {
      // Reset all lights
      elements.redLight.classList.remove('active');
      elements.yellowLight.classList.remove('active');
      elements.greenLight.classList.remove('active');
      
      const trafficIntensity = getTrafficStatus(vehicleCount);
      state.currentGreenTime = getGreenLightDuration(trafficIntensity);
      
      // Set the current light state
      if (state.currentLightState === LIGHT_STATES.GREEN) {
        elements.greenLight.classList.add('active');
        state.timerValue = state.currentGreenTime;
      } else if (state.currentLightState === LIGHT_STATES.YELLOW) {
        elements.yellowLight.classList.add('active');
      } else {
        elements.redLight.classList.add('active');
      }
      
      elements.lightTimer.textContent = state.timerValue;
    }
    
    function updateTimer() {
      if (state.timerValue > 0) {
        state.timerValue--;
        elements.lightTimer.textContent = state.timerValue;
      } else {
        // Transition to next light state
        if (state.currentLightState === LIGHT_STATES.GREEN) {
          // Green -> Yellow
          state.currentLightState = LIGHT_STATES.YELLOW;
          elements.greenLight.classList.remove('active');
          elements.yellowLight.classList.add('active');
          state.timerValue = 3;
        } else if (state.currentLightState === LIGHT_STATES.YELLOW) {
          // Yellow -> Red
          state.currentLightState = LIGHT_STATES.RED;
          elements.yellowLight.classList.remove('active');
          elements.redLight.classList.add('active');
          state.timerValue = 10;
        } else {
          // Red -> Green
          state.currentLightState = LIGHT_STATES.GREEN;
          elements.redLight.classList.remove('active');
          elements.greenLight.classList.add('active');
          state.timerValue = state.currentGreenTime;
        }
      }
    }
    
    function getGreenLightDuration(trafficIntensity) {
      const intensityMap = {
        "Avtomobil yo'q": 0,
        "Juda past": 5,
        "Yengil": 15,
        "O'rtacha": 30,
        "Qattiq": 45,
        "O'ta qattiq": 60
      };
      return intensityMap[trafficIntensity] || 15;
    }
  
    // ======================
    // Traffic Data & Video
    // ======================
    
    function initDataUpdates() {
      updateVideoFeed();
      fetchTrafficData();
      
      state.intervals.video = setInterval(updateVideoFeed, config.updateIntervals.video);
      state.intervals.data = setInterval(fetchTrafficData, config.updateIntervals.data);
      state.intervals.location = setInterval(updateLocation, config.updateIntervals.location);
    }
    
    function updateVideoFeed() {
      const timestamp = new Date().getTime();
      elements.videoFeed.src = `/frame.jpg?t=${timestamp}`;
      
      // Show loading indicator while new image loads
      elements.loadingIndicator.style.display = 'flex';
      elements.videoFeed.onload = () => {
        elements.loadingIndicator.style.display = 'none';
      };
      
      elements.videoFeed.onerror = () => {
        elements.loadingIndicator.innerHTML = '<i class="fas fa-exclamation-triangle"></i> <span>Kamera ulanmadi</span>';
      };
    }
    
    async function fetchTrafficData() {
      try {
        // In a real implementation, this would fetch from your API
        // For demo purposes, we'll simulate data
        const vehicleCount = Math.floor(Math.random() * 100);
        const trafficIntensity = getTrafficStatus(vehicleCount);
        
        // Update UI with new data
        updateUI(vehicleCount, trafficIntensity);
        
        // Update traffic light based on traffic
        updateTrafficLight(vehicleCount);
        
      } catch (error) {
        console.error('Trafik ma\'lumotlarini olishda xato:', error);
      }
    }
    
    function updateUI(vehicleCount, trafficIntensity) {
      elements.vehicleCount.textContent = vehicleCount;
      elements.trafficStatus.textContent = trafficIntensity;
      elements.carCount.textContent = Math.floor(vehicleCount * 0.7);
      elements.busCount.textContent = Math.floor(vehicleCount * 0.15);
      elements.truckCount.textContent = Math.floor(vehicleCount * 0.1);
      elements.motorcycleCount.textContent = Math.floor(vehicleCount * 0.05);
    }
    
    function getTrafficStatus(vehicleCount) {
      if (vehicleCount === 0) return "Avtomobil yo'q";
      if (vehicleCount < 5) return "Juda past";
      if (vehicleCount < 15) return "Yengil";
      if (vehicleCount < 40) return "O'rtacha";
      if (vehicleCount < 70) return "Qattiq";
      return "O'ta qattiq";
    }
    
    function updateLocation() {
      elements.locationStatus.textContent = config.locations[state.currentLocationIndex];
      state.currentLocationIndex = (state.currentLocationIndex + 1) % config.locations.length;
    }
  
    // ======================
    // Public Methods
    // ======================
    
    return {
      init: function() {
        console.log("Yo'lNigoh AI Traffic System initializing...");
        initNavigation();
        initTrafficLight();
        initDataUpdates();
        updateLocation(); // Set initial location
      },
      
      // For future expansion
      getState: function() {
        return state;
      },
      
      updateConfig: function(newConfig) {
        Object.assign(config, newConfig);
      }
    };
  })();
  
  // Initialize the system when DOM is loaded
  document.addEventListener('DOMContentLoaded', () => {
    TrafficSystem.init();
  });