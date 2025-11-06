# 🇹🇭 Thailand Essential Apps

A curated guide to the **must-have apps for travelers, expats, and digital nomads in Thailand**. This Jekyll-based documentation site provides comprehensive information about essential mobile applications, including their purpose, best use cases, hidden tricks, and download links.

## 📋 Project Overview

**Purpose**: Help travelers, expats, and digital nomads quickly discover and set up essential apps for living in Thailand.

**Target Audience**: 
- Travelers visiting Thailand
- Expats living in Thailand
- Digital nomads working remotely from Thailand

**Key Features**:
- Categorized app recommendations with detailed descriptions
- Visual app screenshots and icons
- Setup instructions for Thai App Store/Google Play access
- Mobile-optimized documentation site
- Search functionality
- Clean, modern UI with Just the Docs theme

## 🏗️ Technical Architecture

### Technology Stack
- **Static Site Generator**: Jekyll 4.3.0
- **Theme**: Just the Docs (GitHub Pages compatible)
- **CSS**: Custom styling with SCSS support
- **Deployment**: GitHub Pages ready

### Project Structure
```
thailand-essentials-apps/
├── _config.yml              # Jekyll configuration
├── _includes/               # Jekyll includes
│   └── custom-head.html     # Custom head elements
├── _layouts/                # Jekyll layouts (theme-based)
├── assets/                  # Static assets
│   └── css/
│       └── style.css        # Custom CSS styling
├── icons/                   # App icons (64x64px)
│   ├── agoda.jpg
│   ├── airbnb.jpg
│   ├── grab.jpg
│   └── ... (24 total icons)
├── screenshots/             # App screenshots (156x277px)
│   ├── agoda-1.jpg
│   ├── agoda-2.jpg
│   ├── agoda-3.jpg
│   └── ... (72 total screenshots)
├── index.md                 # Homepage
├── transport.md             # Transport & Navigation apps
├── money.md                 # Money & Payment apps
├── food.md                  # Food & Grocery apps
├── housing.md               # Accommodation apps
├── social.md                # Communication & Social apps
├── shopping.md              # Shopping & Lifestyle apps
└── README.md                # This file
```

## 📱 App Categories

### 1. Transport & Navigation (`transport.md`)
- **Google Maps**: Navigation and local business discovery
- **Apple Maps**: iOS navigation alternative
- **Grab**: Ride-hailing and food delivery
- **Bolt**: Alternative ride-hailing service
- **BTS SkyTrain**: Bangkok public transport
- **Bangkok MRT**: Bangkok metro system

### 2. Money & Payments (`money.md`)
- **TrueMoney Wallet**: Thai digital wallet and QR payments
- **Moreta Pay**: Alternative payment solution
- **Wise**: International money transfers
- **Revolut**: Multi-currency banking

### 3. Food & Groceries (`food.md`)
- **GrabFood**: Food delivery service
- **LINE MAN Wongnai**: Food delivery and restaurant discovery
- **Makro PRO**: Wholesale grocery shopping

### 4. Accommodation & Housing (`housing.md`)
- **Airbnb**: Short-term rentals
- **Agoda**: Hotel and accommodation booking
- **Booking.com**: Global accommodation platform

### 5. Communication & Social (`social.md`)
- **LINE**: Primary messaging app in Thailand
- **Messenger**: Facebook messaging
- **WhatsApp**: International messaging

### 6. Shopping & Lifestyle (`shopping.md`)
- **Shopee**: E-commerce platform
- **Lazada**: Online shopping marketplace

## 🎨 Design System

### Screenshot Specifications
- **Dimensions**: 156px × 277px (30% larger than original 120px × 213px)
- **Format**: JPG
- **Style**: Rounded corners (10px), drop shadow, hover scale effect
- **Layout**: Horizontal scrollable container with 0.75rem gaps

### Icon Specifications
- **Dimensions**: 64px × 64px
- **Format**: JPG/PNG
- **Style**: Rounded corners (8px), subtle drop shadow
- **Usage**: Centered above app titles

### Color Scheme
- **Theme**: Just the Docs light theme
- **Custom CSS**: Additional styling in `assets/css/style.css`
- **Responsive**: Mobile-first design approach

## 🚀 Development Setup

### Prerequisites
- Ruby 2.7+ (for Jekyll)
- Git
- Local Jekyll environment (for example `gem install github-pages webrick`)

### Local Development

```bash
# Clone the repository
git clone https://github.com/jdelaire/thailand-essentials-apps.git
cd thailand-essentials-apps

# Install GitHub Pages-compatible Jekyll tooling (first run only)
gem install github-pages webrick

# Serve locally
jekyll serve

# Access at http://localhost:4000
```

### Development Commands
```bash
# Serve with live reload
jekyll serve --livereload

# Build for production
jekyll build

# Clean build artifacts
jekyll clean
```

## 📝 Content Management

### Adding New Apps

1. **Prepare Assets**:
   - Create app icon (64×64px) → save to `icons/`
   - Take 3 screenshots (156×277px) → save to `screenshots/`

2. **Update Category File**:
   - Add app section to appropriate `.md` file
   - Follow existing structure with app header, description, and screenshots

3. **Structure Template**:
```markdown
<div class="app-header">
  <img src="icons/app-name.jpg" alt="App Name icon" width="64" height="64" class="app-icon"/>
  <h3 class="app-title">App Name</h3>
</div>

**Purpose**: Brief description of what the app does.

**Best for**: Specific use cases and target users.

**Hidden tricks**: Advanced features and tips.

**Download**: [iOS](link) | [Android](link)

<div class="app-screenshots">
  <img src="screenshots/app-name-1.jpg" alt="App Name Screenshot 1" class="app-screenshot"/>
  <img src="screenshots/app-name-2.jpg" alt="App Name Screenshot 2" class="app-screenshot"/>
  <img src="screenshots/app-name-3.jpg" alt="App Name Screenshot 3" class="app-screenshot"/>
</div>
```

### Modifying Styling

- **Global CSS**: Edit `assets/css/style.css`
- **Page-specific CSS**: Add `<style>` blocks in individual `.md` files
- **Theme customization**: Modify `_config.yml` for Just the Docs settings

### Screenshot Management

- **Current Size**: 156px × 277px (30% increase from original 120px × 213px)
- **To resize**: Update both `assets/css/style.css` and inline styles in all `.md` files
- **Naming Convention**: `{app-name}-{1,2,3}.jpg`

## 🔧 Configuration

### Jekyll Configuration (`_config.yml`)
- **Theme**: Just the Docs with light color scheme
- **Search**: Enabled with custom tokenizer
- **Plugins**: jekyll-remote-theme, jekyll-sass-converter, jekyll-feed
- **Custom CSS**: Linked via head_scripts

## 🚀 Deployment

### GitHub Pages
The site is configured for automatic deployment via GitHub Pages:

1. Push changes to `main` branch
2. GitHub Pages automatically builds and deploys
3. Site available at: `https://username.github.io/thailand-essentials-apps`

### Manual Deployment
```bash
# Build for production
jekyll build

# Deploy _site/ directory to your web server
```

## 📊 Performance Considerations

### Image Optimization
- **Icons**: 64×64px, optimized JPG/PNG
- **Screenshots**: 156×277px, compressed JPG
- **Lazy Loading**: Consider implementing for better performance

### Site Performance
- **Static Generation**: Fast loading with Jekyll
- **CDN**: GitHub Pages provides global CDN
- **Compression**: SCSS compiled with compression enabled

## 🔍 SEO & Accessibility

### SEO Features
- **Meta Tags**: Title and description configured
- **Structured Data**: Markdown provides semantic structure
- **Search**: Built-in search functionality
- **Sitemap**: Auto-generated by jekyll-sitemap

### Accessibility
- **Alt Text**: All images include descriptive alt text
- **Semantic HTML**: Proper heading hierarchy
- **Keyboard Navigation**: Just the Docs theme supports keyboard navigation
- **Screen Reader**: Compatible with assistive technologies

## 🛠️ Maintenance Tasks

### Regular Updates
- **App Information**: Keep descriptions and links current
- **Screenshots**: Update when apps change UI significantly
- **New Apps**: Add emerging essential apps
- **Dependencies**: Keep Jekyll and gems updated

### Quality Assurance
- **Link Checking**: Verify all download links work
- **Image Optimization**: Ensure all images are properly sized
- **Content Review**: Check for outdated information
- **Mobile Testing**: Verify responsive design on various devices

## 🤝 Contributing

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `jekyll serve`
5. Submit a pull request

### Contribution Guidelines
- Follow existing content structure and style
- Ensure all images are properly optimized
- Test changes on mobile devices
- Update this README if adding new features

## 📄 License

This project is licensed under the [MIT License](LICENSE). You're free to use, share, and adapt with attribution.

## 👥 Credits

Created and maintained by [@jdelaire](https://github.com/jdelaire). Special focus on tools and apps that make life easier for **expats, digital nomads, and travelers in Thailand**.

---

## 🔗 Quick Links

- **Live Site**: [GitHub Pages URL]
- **Repository**: [GitHub Repository URL]
- **Issues**: [GitHub Issues URL]
- **Contributing**: See Contributing section above

---

*Last updated: [Current Date]*
*Jekyll Version: 4.3.0*
*Theme: Just the Docs*
