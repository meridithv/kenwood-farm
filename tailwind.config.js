module.exports = {
  content: ["./farm_chat/templates/*.{html,js}"],
  theme: {
     colors: {
      forest: '#242D24',
      ecru: '#F9F4EB',
      darkcru: '#E8DDC7',
      anguilla: '#1A87A1',
      tahiti: '#40B5C3',
      pool: '#7EC8C1',
      wine: '#6D000A',
      mulberry: '#AD002B',
      mauve: '#AD4141',
      rust: '#C82813',
      fever: '#E51219',
      longhorn: '#D6491C',
      clem: '#FA831F',
      marigold: '#FA9D2C',
      creamsoda: '#FFF5CB',
      white: '#FFFFFF',
      black: '000000',
      greener: '#0BDA51'
    },
    screens: {
      sm:'480px',
      md:'868px',
      lg:'976px',
      xl:'1440px'
    },
    extend: {
      fontFamily: {
        plex: ['IBM Plex Sans', 'sans-serif'],
        libre: ['Libre Baskerville', 'serif'],
        bitter: ['Bitter', 'serif'],
        bungee: ['Bungee', 'sans-serif'],
        yeseva: ['Yeseva One', 'serif'],
        patrick: ['Patrick Hand SC', 'sans-serif']
      },
    }
  }
}