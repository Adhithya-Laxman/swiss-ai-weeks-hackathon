// Mario's World Adventure Game
class MarioAdventure {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.gameStarted = false;
        this.mushroomCount = 0;
        this.completedLocations = 0;
        this.totalLocations = 4;
        
        // Location data from JSON input - positioned on the world map
        this.locations = {
            '🔥': { name: 'Bolivia', x: 100, y: 280, completed: false },
            '🪨': { name: 'Afghanistan', x: 580, y: 180, completed: false },
            '🌧️': { name: 'Yemen', x: 530, y: 200, completed: false },
            '🦟': { name: 'Congo', x: 320, y: 280, completed: false }
        };
        
        // Disaster titles mapping
        this.disasterTitles = {
            'Bolivia': "Bolivia Wildfires: Relief Phase Initiated",
            'Afghanistan': "Earthquake in Nangarhar Province, Afghanistan",
            'Yemen': "Southern Yemen Flooding - Response Overview",
            'Congo': "Ebola Outbreak in Democratic Republic of Congo"
        };
        
        // Mario's house position (bottom left)
        this.marioHouse = { x: 50, y: 520 };
        
        // Castle position (bottom right)
        this.castle = { x: 750, y: 520 };
        
        // Mario character properties - start from house
        this.mario = {
            x: 50,
            y: 520,
            width: 32,
            height: 32,
            targetX: 50,
            targetY: 520,
            moving: false,
            speed: 2
        };
        
        // Sound system
        this.sounds = {
            jump: null,
            end: null,
            support: null,
            start: null
        };
        
        this.loadSounds();
        
        this.init();
    }
    
    loadSounds() {
        // Load sound files (you'll need to add these MP3 files to your project)
        this.sounds.jump = new Audio('sounds/Jump.mp3');
        this.sounds.end = new Audio('sounds/End.mp3');
        this.sounds.support = new Audio('sounds/Support.mp3');
        this.sounds.start = new Audio('sounds/End.mp3');
        
        // Set volume levels
        Object.values(this.sounds).forEach(sound => {
            if (sound) {
                sound.volume = 0.5; // Adjust volume as needed
            }
        });
    }
    
    playSound(soundName) {
        if (this.sounds[soundName]) {
            this.sounds[soundName].currentTime = 0; // Reset to beginning
            this.sounds[soundName].play().catch(e => {
                console.log('Sound play failed:', e); // Handle autoplay restrictions
            });
        }
    }
    
    init() {
        this.setupEventListeners();
        this.setupCanvas();
        this.loadWorldMapImage();
        this.gameLoop();
        
        // Play start sound when game initializes
        setTimeout(() => {
            this.playSound('start');
        }, 1500);
    }
    
    setupCanvas() {
        // Ensure pixel-perfect rendering
        this.ctx.imageSmoothingEnabled = false;
        this.ctx.webkitImageSmoothingEnabled = false;
        this.ctx.mozImageSmoothingEnabled = false;
        this.ctx.msImageSmoothingEnabled = false;
    }
    
    setupEventListeners() {
        // Start button
        document.getElementById('startButton').addEventListener('click', () => {
            this.startGame();
        });
        
        // Support button
        document.getElementById('supportButton').addEventListener('click', () => {
            this.showCompletionPopup();
        });
        
        // Chat button
        document.getElementById('chatButton').addEventListener('click', () => {
            this.closeChat();
        });
        
        // Completion popup close
        document.getElementById('completionPopup').addEventListener('click', () => {
            this.closeCompletionPopup();
        });
        
        // OK button (now "Lets Go!" button)
        document.getElementById('okButton').addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent event bubbling
            this.closeCompletionPopup();
            // Move Mario to the castle when "Lets Go!" is pressed
            this.moveMarioToCastle();
        });
        
        // Refresh button
        document.getElementById('refreshButton').addEventListener('click', () => {
            this.refreshGame();
        });
    }
    
    startGame() {
        this.gameStarted = true;
        document.getElementById('startButton').style.display = 'none';
        document.getElementById('speechBubble').style.display = 'block';
        
        // Play start sound
        this.playSound('start');
        
        // Show emojis on the map
        this.showEmojis();
        
        // Hide speech bubble after 5 seconds (longer duration)
        setTimeout(() => {
            document.getElementById('speechBubble').style.display = 'none';
        }, 5000);
    }
    
    showEmojis() {
        const emojiContainer = document.getElementById('emojiContainer');
        
        Object.entries(this.locations).forEach(([emoji, location]) => {
            // Create sparkle container
            const sparkleContainer = document.createElement('div');
            sparkleContainer.className = 'sparkle-container';
            sparkleContainer.style.position = 'absolute';
            sparkleContainer.style.left = (location.x - 15) + 'px';
            sparkleContainer.style.top = (location.y - 15) + 'px';
            sparkleContainer.style.width = '50px';
            sparkleContainer.style.height = '50px';
            sparkleContainer.style.pointerEvents = 'none';
            sparkleContainer.style.zIndex = '4';
            
            // Add golden sparkles
            this.addSparkles(sparkleContainer);
            
            // Create emoji element
            const emojiElement = document.createElement('div');
            emojiElement.className = 'emoji-location';
            emojiElement.textContent = emoji;
            emojiElement.setAttribute('data-emoji', emoji);
            emojiElement.style.left = '15px';
            emojiElement.style.top = '15px';
            emojiElement.style.position = 'absolute';
            emojiElement.addEventListener('click', () => {
                this.moveToLocation(emoji, location);
            });
            
            sparkleContainer.appendChild(emojiElement);
            emojiContainer.appendChild(sparkleContainer);
        });
    }
    
    addSparkles(container) {
        // Create white and yellow sparkles around the emoji
        const sparkleCount = 12; // More sparkles for better effect
        for (let i = 0; i < sparkleCount; i++) {
            const sparkle = document.createElement('div');
            sparkle.className = 'sparkle';
            sparkle.style.position = 'absolute';
            sparkle.style.width = '6px'; // Bigger sparkles
            sparkle.style.height = '6px';
            sparkle.style.borderRadius = '50%';
            sparkle.style.animation = `sparkle 2s infinite ${i * 0.15}s`;
            
            // Alternate between white and yellow
            if (i % 2 === 0) {
                sparkle.style.backgroundColor = '#ffffff';
                sparkle.style.boxShadow = '0 0 4px #ffffff';
            } else {
                sparkle.style.backgroundColor = '#ffd700';
                sparkle.style.boxShadow = '0 0 4px #ffd700';
            }
            
            // Position sparkles in a circle around the emoji
            const angle = (i / sparkleCount) * 2 * Math.PI;
            const radius = 25; // Slightly larger radius
            const x = 25 + Math.cos(angle) * radius;
            const y = 25 + Math.sin(angle) * radius;
            
            sparkle.style.left = x + 'px';
            sparkle.style.top = y + 'px';
            
            container.appendChild(sparkle);
        }
    }
    
    moveToLocation(emoji, location) {
        if (this.mario.moving) return;
        
        // Play jump sound
        this.playSound('jump');
        
        this.mario.targetX = location.x - 16; // Center Mario on emoji
        this.mario.targetY = location.y - 16;
        this.mario.moving = true;
        
        // Don't hide emoji when clicked - keep it visible
        // const emojiElement = document.querySelector(`[data-emoji="${emoji}"]`);
        // if (emojiElement) {
        //     emojiElement.style.display = 'none';
        // }
        
        // Show chat after movement
        setTimeout(() => {
            this.showChat(emoji, location);
        }, 1000);
    }
    
    showChat(emoji, location) {
        const chatModal = document.getElementById('chatModal');
        const chatText = document.getElementById('chatText');
        
        // Store current location for printing disaster title
        this.currentLocation = location;
        
        let chatContent = '';
        if (emoji === '🔥') {
            chatContent = `Welcome to Bolivia! 🇧🇴<br><br>
            The devastating wildfires have destroyed thousands of hectares 
            of forest and displaced many families. We need immediate 
            support for emergency relief and recovery efforts. 
            Can you help us?`;
        } else if (emoji === '🪨') {
            chatContent = `Welcome to Afghanistan! 🇦🇫<br><br>
            A powerful earthquake has struck Nangarhar Province, 
            causing widespread destruction and loss of life. 
            We need urgent assistance for rescue operations and 
            humanitarian aid. Can you help us?`;
        } else if (emoji === '🌧️') {
            chatContent = `Welcome to Yemen! 🇾🇪<br><br>
            Severe flooding has devastated southern Yemen, 
            destroying homes and infrastructure. Many families 
            are in desperate need of shelter, food, and medical 
            assistance. Can you help us?`;
        } else if (emoji === '🦟') {
            chatContent = `Welcome to Democratic Republic of Congo! 🇨🇩<br><br>
            A new Ebola outbreak has emerged, threatening 
            communities across the region. We need immediate 
            support for medical supplies, healthcare workers, 
            and containment efforts. Can you help us?`;
        }
        
        chatText.innerHTML = chatContent;
        chatModal.style.display = 'flex';
        
        // Mark location as completed
        location.completed = true;
        this.completedLocations++;
    }
    
    closeChat() {
        document.getElementById('chatModal').style.display = 'none';
        
        // Print the disaster title when Continue button is pressed
        if (this.currentLocation && this.disasterTitles[this.currentLocation.name]) {
            console.log(this.disasterTitles[this.currentLocation.name]);
            alert(this.disasterTitles[this.currentLocation.name]);
        }
        
        // Show support button when user clicks "Continue"
        this.showSupportButton();
    }
    
    showSupportButton() {
        document.getElementById('supportButton').style.display = 'block';
    }
    
    showCompletionPopup() {
        // Play support sound
        this.playSound('support');
        
        this.mushroomCount += 5;
        document.getElementById('mushroomCount').textContent = this.mushroomCount;
        document.getElementById('mushroomPower').style.display = 'block';
        document.getElementById('completionPopup').style.display = 'block';
        document.getElementById('supportButton').style.display = 'none';
    }
    
    moveMarioToCastle() {
        // Make Mario go to the castle when "Lets Go!" is pressed
        this.mario.targetX = this.castle.x - 16;
        this.mario.targetY = this.castle.y - 16;
        this.mario.moving = true;
        
        // Show Princess Peach dialogue after Mario reaches castle
        setTimeout(() => {
            this.showPrincessPeachDialogue();
        }, 2000);
    }
    
    closeCompletionPopup() {
        document.getElementById('completionPopup').style.display = 'none';
    }
    
    showPrincessPeachDialogue() {
        // Play end sound
        this.playSound('end');
        
        // Show Princess Peach dialogue
        const speechBubble = document.getElementById('speechBubble');
        speechBubble.innerHTML = 'Hope to see you soon Princess Peach 👑';
        speechBubble.style.display = 'block';
        
        // Show refresh button after dialogue
        setTimeout(() => {
            speechBubble.style.display = 'none';
            document.getElementById('refreshButton').style.display = 'block';
        }, 4000);
    }
    
    refreshGame() {
        // Reset game state
        this.gameStarted = false;
        this.mushroomCount = 0;
        this.completedLocations = 0;
        
        // Reset Mario position to house
        this.mario.x = 50;
        this.mario.y = 520;
        this.mario.targetX = 50;
        this.mario.targetY = 520;
        this.mario.moving = false;
        
        // Reset locations
        Object.values(this.locations).forEach(location => {
            location.completed = false;
        });
        
        // Hide all UI elements
        document.getElementById('startButton').style.display = 'block';
        document.getElementById('supportButton').style.display = 'none';
        document.getElementById('speechBubble').style.display = 'none';
        document.getElementById('mushroomPower').style.display = 'none';
        document.getElementById('refreshButton').style.display = 'none';
        document.getElementById('completionPopup').style.display = 'none';
        document.getElementById('chatModal').style.display = 'none';
        
        // Clear emoji container
        document.getElementById('emojiContainer').innerHTML = '';
        
        // Play start sound
        this.playSound('start');
    }
    
    drawWorldMap() {
        // Draw the provided pixel art world map as background
        if (this.worldMapImage) {
            this.ctx.drawImage(this.worldMapImage, 0, 0, this.canvas.width, this.canvas.height);
        } else {
            // Fallback: solid blue background if image not loaded
            this.ctx.fillStyle = '#0066cc';
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        }
    }
    
    loadWorldMapImage() {
        const img = new Image();
        img.onload = () => {
            this.worldMapImage = img;
        };
        // We'll create the image data from the description
        this.createWorldMapFromDescription();
    }
    
    createWorldMapFromDescription() {
        // Create a canvas to draw the world map based on the description
        const mapCanvas = document.createElement('canvas');
        mapCanvas.width = 800;
        mapCanvas.height = 600;
        const mapCtx = mapCanvas.getContext('2d');
        
        // Set pixelated rendering
        mapCtx.imageSmoothingEnabled = false;
        
        // Fill with ocean blue background
        mapCanvas.fillStyle = '#0066cc';
        mapCtx.fillRect(0, 0, 800, 600);
        
        // Draw continents with proper colors
        this.drawWorldMapContinents(mapCtx);
        
        // Convert to image
        this.worldMapImage = new Image();
        this.worldMapImage.src = mapCanvas.toDataURL();
    }
    
    drawWorldMapContinents(ctx) {
        // Create a much more detailed and accurate world map
        
        // North America - more detailed shape
        ctx.fillStyle = '#4a7c59';
        this.drawNorthAmerica(ctx);
        
        // South America - better shape
        ctx.fillStyle = '#4a7c59';
        this.drawSouthAmerica(ctx);
        
        // Europe - more detailed
        ctx.fillStyle = '#4a7c59';
        this.drawEurope(ctx);
        
        // Africa - better shape with Sahara
        this.drawAfrica(ctx);
        
        // Asia - more detailed
        this.drawAsia(ctx);
        
        // Australia - better shape
        this.drawAustralia(ctx);
        
        // Ice caps
        ctx.fillStyle = '#ffffff';
        this.drawIceCaps(ctx);
        
        // Add clouds
        this.drawClouds(ctx);
        
        // Add Mario elements
        this.drawMarioWorldElements(ctx);
    }
    
    drawNorthAmerica(ctx) {
        // Main North America body
        ctx.fillRect(40, 60, 180, 140);
        
        // Alaska
        ctx.fillRect(20, 40, 60, 40);
        
        // Canada extension
        ctx.fillRect(80, 50, 100, 30);
        
        // Mexico/Central America
        ctx.fillRect(60, 200, 80, 40);
        
        // Desert areas in southwest
        ctx.fillStyle = '#f4e4bc';
        ctx.fillRect(80, 140, 60, 40);
        ctx.fillRect(100, 160, 40, 20);
        
        // Reset to green
        ctx.fillStyle = '#4a7c59';
    }
    
    drawSouthAmerica(ctx) {
        // Main body
        ctx.fillRect(80, 250, 100, 120);
        
        // Northern extension
        ctx.fillRect(100, 240, 60, 20);
        
        // Southern tip
        ctx.fillRect(90, 370, 40, 20);
    }
    
    drawEurope(ctx) {
        // Main Europe
        ctx.fillRect(300, 100, 120, 80);
        
        // British Isles
        ctx.fillRect(280, 120, 20, 30);
        
        // Scandinavian extension
        ctx.fillRect(320, 80, 40, 30);
        
        // Eastern Europe
        ctx.fillRect(420, 110, 40, 60);
    }
    
    drawAfrica(ctx) {
        // Main Africa body
        ctx.fillStyle = '#4a7c59';
        ctx.fillRect(320, 200, 100, 120);
        
        // Northern extension
        ctx.fillRect(340, 180, 60, 30);
        
        // Southern tip
        ctx.fillRect(350, 320, 40, 20);
        
        // Sahara desert
        ctx.fillStyle = '#f4e4bc';
        ctx.fillRect(320, 200, 100, 40);
        ctx.fillRect(340, 180, 60, 20);
        
        // Reset to green
        ctx.fillStyle = '#4a7c59';
    }
    
    drawAsia(ctx) {
        // Main Asia
        ctx.fillStyle = '#4a7c59';
        ctx.fillRect(500, 80, 180, 140);
        
        // Middle East
        ctx.fillRect(480, 200, 40, 60);
        
        // Indian subcontinent
        ctx.fillRect(520, 250, 60, 40);
        
        // Southeast Asia
        ctx.fillRect(580, 280, 40, 30);
        
        // Desert areas
        ctx.fillStyle = '#f4e4bc';
        ctx.fillRect(600, 120, 80, 40);
        ctx.fillRect(520, 200, 40, 30);
        
        // Reset to green
        ctx.fillStyle = '#4a7c59';
    }
    
    drawAustralia(ctx) {
        // Main Australia
        ctx.fillStyle = '#f4e4bc';
        ctx.fillRect(600, 300, 100, 60);
        
        // Eastern green area
        ctx.fillStyle = '#4a7c59';
        ctx.fillRect(620, 320, 40, 20);
        ctx.fillRect(650, 310, 30, 30);
        
        // Tasmania
        ctx.fillRect(650, 360, 20, 15);
    }
    
    drawIceCaps(ctx) {
        // Greenland
        ctx.fillRect(200, 20, 80, 50);
        
        // Arctic regions
        ctx.fillRect(300, 20, 200, 30);
        ctx.fillRect(100, 30, 100, 20);
        
        // Antarctica
        ctx.fillRect(400, 400, 200, 60);
        ctx.fillRect(300, 420, 100, 40);
    }
    
    drawClouds(ctx) {
        ctx.fillStyle = '#ffffff';
        
        // Cloud positions
        const clouds = [
            [150, 50], [250, 30], [400, 40], [550, 60],
            [200, 150], [350, 170], [500, 180], [650, 160],
            [100, 250], [300, 280], [450, 300], [600, 320]
        ];
        
        clouds.forEach(([x, y]) => {
            this.drawCloud(ctx, x, y);
        });
    }
    
    drawCloud(ctx, x, y) {
        // Draw a pixelated cloud
        ctx.fillRect(x, y, 8, 4);
        ctx.fillRect(x-2, y-2, 4, 2);
        ctx.fillRect(x+6, y-2, 4, 2);
        ctx.fillRect(x+2, y-4, 4, 2);
    }
    
    drawMarioWorldElements(ctx) {
        // Bottom platform (brown brick with detailed pattern)
        ctx.fillStyle = '#8b4513';
        ctx.fillRect(0, 550, 800, 50);
        
        // Add brick pattern
        ctx.fillStyle = '#6b3410';
        for (let x = 0; x < 800; x += 20) {
            for (let y = 550; y < 600; y += 10) {
                if ((x / 20 + y / 10) % 2 === 0) {
                    ctx.fillRect(x, y, 20, 10);
                }
            }
        }
        
        // Green hill on left with more detail
        ctx.fillStyle = '#4a7c59';
        ctx.fillRect(20, 520, 80, 30);
        // Hill slope
        ctx.fillRect(15, 530, 10, 20);
        ctx.fillRect(10, 535, 10, 15);
        
        // Hill details (grass texture)
        ctx.fillStyle = '#3d6b4a';
        for (let i = 0; i < 8; i++) {
            ctx.fillRect(25 + i * 8, 525, 4, 4);
        }
        ctx.fillRect(30, 530, 4, 4);
        ctx.fillRect(50, 530, 4, 4);
        
        // Green pipe with more detail
        ctx.fillStyle = '#4a7c59';
        ctx.fillRect(120, 500, 24, 50);
        // Pipe top
        ctx.fillStyle = '#3d6b4a';
        ctx.fillRect(115, 495, 34, 10);
        // Pipe rings
        ctx.fillStyle = '#2d5016';
        ctx.fillRect(120, 510, 24, 2);
        ctx.fillRect(120, 525, 24, 2);
        ctx.fillRect(120, 540, 24, 2);
        
        // Castle on right with more detail
        ctx.fillStyle = '#8b4513';
        ctx.fillRect(700, 480, 90, 70);
        
        // Castle tower
        ctx.fillRect(720, 460, 50, 90);
        
        // Castle windows
        ctx.fillStyle = '#000000';
        ctx.fillRect(730, 500, 8, 12);
        ctx.fillRect(750, 500, 8, 12);
        ctx.fillRect(740, 480, 8, 12);
        
        // Castle door
        ctx.fillRect(745, 520, 10, 20);
        
        // Castle battlements
        ctx.fillStyle = '#8b4513';
        for (let i = 0; i < 9; i++) {
            ctx.fillRect(700 + i * 10, 470, 5, 10);
        }
        for (let i = 0; i < 5; i++) {
            ctx.fillRect(720 + i * 10, 450, 5, 10);
        }
        
        // Castle flag
        ctx.fillStyle = '#ff0000';
        ctx.fillRect(770, 460, 20, 15);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(775, 465, 10, 5);
        
        // Trees on continents with better detail
        this.drawTreesOnContinents(ctx);
        
        // Mountains with better detail
        this.drawMountains(ctx);
        
        // Mushrooms (power-ups) with better detail
        this.drawMushrooms(ctx);
        
        // Add some coins scattered around
        this.drawCoins(ctx);
        
        // Draw Mario's house at bottom left
        this.drawMarioHouse(ctx);
    }
    
    drawMarioHouse(ctx) {
        // House base
        ctx.fillStyle = '#8b4513';
        ctx.fillRect(40, 520, 40, 30);
        
        // House roof
        ctx.fillStyle = '#ff0000';
        ctx.fillRect(35, 510, 50, 15);
        
        // House door
        ctx.fillStyle = '#654321';
        ctx.fillRect(50, 535, 8, 15);
        
        // House window
        ctx.fillStyle = '#87ceeb';
        ctx.fillRect(60, 525, 8, 8);
        
        // Chimney
        ctx.fillStyle = '#8b4513';
        ctx.fillRect(70, 505, 6, 10);
        
        // Smoke
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(72, 500, 2, 5);
        ctx.fillRect(71, 498, 4, 2);
    }
    
    drawTreesOnContinents(ctx) {
        ctx.fillStyle = '#2d5016';
        // Trees positioned on actual land masses
        const treePositions = [
            // North America
            [80, 100], [120, 120], [160, 100], [140, 140], [180, 120],
            // South America
            [120, 280], [150, 300], [180, 320], [140, 350],
            // Europe
            [320, 130], [360, 150], [400, 140], [380, 170],
            // Africa
            [360, 220], [400, 240], [380, 280], [420, 260],
            // Asia
            [520, 120], [560, 140], [600, 130], [580, 160], [620, 150],
            // Australia
            [640, 320], [660, 340], [680, 330]
        ];
        
        treePositions.forEach(([x, y]) => {
            // Tree trunk
            ctx.fillRect(x, y, 6, 10);
            // Tree top (more detailed)
            ctx.fillStyle = '#4a7c59';
            ctx.fillRect(x-3, y-6, 12, 6);
            ctx.fillRect(x-1, y-8, 8, 4);
            // Tree highlights
            ctx.fillStyle = '#5a8c69';
            ctx.fillRect(x-2, y-6, 4, 2);
            ctx.fillStyle = '#2d5016';
        });
    }
    
    drawMountains(ctx) {
        ctx.fillStyle = '#8b7355';
        // Mountains positioned on actual land masses
        const mountainPositions = [
            // North America (Rockies)
            [140, 120], [180, 100], [160, 140],
            // South America (Andes)
            [150, 320], [180, 340],
            // Europe (Alps)
            [360, 140], [400, 160],
            // Africa (Atlas)
            [360, 200], [400, 220],
            // Asia (Himalayas)
            [560, 120], [600, 140], [620, 160],
            // Australia (Great Dividing Range)
            [640, 300]
        ];
        
        mountainPositions.forEach(([x, y]) => {
            // Mountain base
            ctx.fillRect(x, y, 8, 15);
            // Mountain peak
            ctx.fillRect(x+2, y-6, 4, 6);
            // Snow cap
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(x+3, y-4, 2, 2);
            ctx.fillStyle = '#8b7355';
        });
    }
    
    drawMushrooms(ctx) {
        // Mushrooms positioned on actual land masses
        const mushroomPositions = [
            // North America
            [100, 110], [160, 130], [140, 150],
            // South America
            [130, 290], [170, 310],
            // Europe
            [340, 140], [380, 160],
            // Africa
            [370, 230], [410, 250],
            // Asia
            [540, 130], [580, 150], [620, 140],
            // Australia
            [650, 330]
        ];
        
        mushroomPositions.forEach(([x, y]) => {
            // Mushroom cap
            ctx.fillStyle = '#ff0000';
            ctx.fillRect(x, y, 10, 6);
            // Mushroom spots
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(x+2, y+1, 2, 2);
            ctx.fillRect(x+6, y+3, 2, 2);
            // Mushroom stem
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(x+3, y+6, 4, 8);
        });
    }
    
    drawCoins(ctx) {
        ctx.fillStyle = '#ffff00';
        // Coins positioned on actual land masses
        const coinPositions = [
            // North America
            [90, 90], [130, 110], [170, 90], [150, 130],
            // South America
            [110, 270], [150, 290], [170, 310],
            // Europe
            [330, 120], [370, 140], [390, 160],
            // Africa
            [350, 210], [390, 230], [410, 250],
            // Asia
            [530, 110], [570, 130], [610, 120], [590, 150],
            // Australia
            [630, 310], [670, 330]
        ];
        
        coinPositions.forEach(([x, y]) => {
            ctx.fillRect(x, y, 4, 4);
        });
    }
    
    drawMario() {
        // Draw pixelated Mario character
        const x = this.mario.x;
        const y = this.mario.y;
        
        // Mario's body (blue overalls)
        this.ctx.fillStyle = '#0066ff';
        this.ctx.fillRect(x + 4, y + 8, 24, 20);
        
        // Mario's head (skin tone)
        this.ctx.fillStyle = '#ffdbac';
        this.ctx.fillRect(x + 6, y + 2, 20, 16);
        
        // Mario's hat (red)
        this.ctx.fillStyle = '#ff0000';
        this.ctx.fillRect(x + 4, y, 24, 8);
        
        // Mario's mustache (brown)
        this.ctx.fillStyle = '#8b4513';
        this.ctx.fillRect(x + 10, y + 6, 8, 2);
        
        // Mario's eyes
        this.ctx.fillStyle = '#000000';
        this.ctx.fillRect(x + 8, y + 4, 2, 2);
        this.ctx.fillRect(x + 18, y + 4, 2, 2);
        
        // Mario's overalls buttons (yellow)
        this.ctx.fillStyle = '#ffff00';
        this.ctx.fillRect(x + 12, y + 12, 4, 4);
        this.ctx.fillRect(x + 20, y + 12, 4, 4);
        
        // Mario's shoes (brown)
        this.ctx.fillStyle = '#8b4513';
        this.ctx.fillRect(x + 6, y + 28, 8, 4);
        this.ctx.fillRect(x + 18, y + 28, 8, 4);
    }
    
    updateMario() {
        if (this.mario.moving) {
            const dx = this.mario.targetX - this.mario.x;
            const dy = this.mario.targetY - this.mario.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < this.mario.speed) {
                this.mario.x = this.mario.targetX;
                this.mario.y = this.mario.targetY;
                this.mario.moving = false;
            } else {
                this.mario.x += (dx / distance) * this.mario.speed;
                this.mario.y += (dy / distance) * this.mario.speed;
            }
        }
    }
    
    gameLoop() {
        this.updateMario();
        
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Redraw everything
        this.drawWorldMap();
        this.drawMario();
        
        requestAnimationFrame(() => this.gameLoop());
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new MarioAdventure();
});
