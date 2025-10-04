# Quick Start Guide - Integrated Mil Dashboard

## 🚀 Getting Started

### Prerequisites

- Node.js installed
- Backend API running on `http://localhost:8000`

### Installation & Running

```bash
# Navigate to the dashboard
cd mil_dashboard

# Dependencies are already installed
# If you need to reinstall:
# npm install

# Start the development server
npm run dev
```

The dashboard will be available at: **http://localhost:3000**

## 🎯 Features Overview

### 1. **Main Header**

- **TACTICAL OPS DASHBOARD** title
- **SUMMARIZE** button - Opens the operational summary modal
- **Unit Level Selector** - Switch between Brigade/Battalion/Company/Platoon/Squad views

### 2. **Active Units Sidebar** (Left)

- Lists all soldiers from the backend
- Click on a soldier to view their specific data
- Shows soldier name, rank, and unit

### 3. **Live Reports Stream** (Main Area)

- Real-time battlefield reports feed
- Submit new reports using the text input
- Click on any report card to open detailed view in Report Drawer
- Report types: EOINCREP, CASEVAC, SITREP, MEDEVAC, SPOTREP, INTREP
- Priority indicators: FLASH, IMMEDIATE, PRIORITY, ROUTINE

### 4. **Soldier-Specific Data** (Below Stream)

When a soldier is selected:

- **Raw Voice Inputs** - Original voice transcriptions from the soldier
- **AI-Generated Reports** - Structured reports with confidence scores

### 5. **Report Drawer** (Right Slide-in Panel)

Opens when you click on a report, showing:

- Location & GPS coordinates
- Unit and priority information
- Casualty count (for CASEVAC reports)
- Incident timeline chart
- Report log with timestamps

### 6. **Summary Modal** (Center Popup)

Click "SUMMARIZE" button to open:

- Select time span (1h, 6h, 12h, 24h, 48h, 7d)
- Select unit level
- View generated summary with:
  - Total reports count
  - Casualties count
  - Enemy contacts count
  - Report breakdown by type

## 🎨 Design Features

### Dark Theme

- The dashboard uses a military-themed dark color scheme
- Grid background pattern for tactical aesthetic
- Neumorphic design with shadows and depth

### Color Coding

- **Red** - CASEVAC/MEDEVAC (medical emergencies)
- **Yellow/Amber** - EOINCREP/SPOTREP (enemy observations)
- **Blue** - INTREP (intelligence reports)
- **Olive** - SITREP (situation reports)

### Interactive Elements

- Hover effects on all clickable items
- Smooth animations for modal/drawer opening
- Responsive layout for different screen sizes

## 📊 Data Flow

```
Backend API → Dashboard Page Component
                    ↓
        Fetches soldiers, raw inputs, reports
                    ↓
            Displays in UI
                    ↓
        User interactions trigger:
        - Report drawer opening
        - Summary modal opening
        - Soldier selection changes
```

## 🔧 Customization

### Modify Report Stream Data

Edit: `src/components/stream-panel.tsx`

- Update the mock `updates` array to fetch from your backend
- Customize report types and fields

### Change Styling

Edit: `src/app/globals.css`

- Modify CSS variables for colors
- Adjust neumorphic shadow values
- Change military color scheme

### Add New Features

1. Create new components in `src/components/`
2. Import and use in `src/app/page.tsx`
3. Utilize existing UI components from `src/components/ui/`

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Kill process on port 3000
npx kill-port 3000
# Or use a different port
npm run dev -- -p 3001
```

### Backend Connection Issues

- Ensure backend API is running on port 8000
- Check CORS settings if requests are blocked
- Verify API endpoints match expected format

### Styling Issues

- Clear browser cache
- Check if `tw-animate-css` is properly imported
- Verify Tailwind CSS is processing the styles

## 📝 Component Structure

```
src/
├── app/
│   ├── page.tsx          # Main dashboard page
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles with theme
├── components/
│   ├── stream-panel.tsx       # Live reports stream
│   ├── data-stream-selector.tsx  # Unit selector
│   ├── report-drawer.tsx      # Report details drawer
│   ├── summary-modal.tsx      # Summary generation modal
│   └── ui/                    # Reusable UI components
│       ├── button.tsx
│       ├── card.tsx
│       ├── dialog.tsx
│       ├── dropdown-menu.tsx
│       ├── input.tsx
│       ├── label.tsx
│       ├── select.tsx
│       └── chart.tsx
└── lib/
    └── utils.ts          # Utility functions (cn, etc.)
```

## 🚦 Development Workflow

1. **Start Backend** - Ensure your Python backend is running
2. **Start Frontend** - `npm run dev` in mil_dashboard
3. **Make Changes** - Edit components/pages
4. **Hot Reload** - Changes automatically reflect in browser
5. **Build for Production** - `npm run build` when ready

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui Components](https://ui.shadcn.com/)
- [Radix UI Primitives](https://www.radix-ui.com/)
- [Lucide Icons](https://lucide.dev/)

## 💡 Tips

- Use the browser DevTools to inspect components
- Check console for any errors or warnings
- The dashboard is fully responsive - try different screen sizes
- Dark mode is enabled by default via the `dark` class on the root div
