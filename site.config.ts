export const siteConfig = {
  // TODO-CLAUDE: replace with the approved production URL before deployment.
  url: 'http://localhost:4321',
  language: 'en',
  title: 'Jonathan Dolan | Support & Operations',
  description: 'Customer support operations, application support, and personal projects built with AI coding agents under my direction and review.',
  author: {
    name: 'Jonathan Dolan',
    title: 'Reliability, troubleshooting & support operations.',
    bio: 'I worked in customer support at Wolt from 2022 to 2024, including Shift Manager responsibilities. I completed Coding Academy’s full-stack bootcamp in 2024. I direct AI coding agents to build and run a personal assistant on a home Linux server. I am looking for an application or product support role in Israel.',
    email: 'yonidolan1@gmail.com',
    location: 'Ramat Gan, Israel',
  },
  social: {
    github: 'https://github.com/JonathanDolan1',
    linkedin: 'https://www.linkedin.com/in/jonathan-dolan-329496374',
    twitter: '',
    mastodon: '',
    bluesky: '',
  },
  nav: [
    { label: 'Projects', href: '/projects/' },
    { label: 'About', href: '/#about' },
    { label: 'Skills', href: '/#skills' },
    { label: 'Contact', href: '/#contact' },
  ],
  resume: '/resume.pdf',
  aiTools: 'AI Tools: Claude Code, Codex / ChatGPT, Claude API',
  supportSkills: ['Escalation handling', 'Case prioritization', 'Shift coordination', 'Service-quality monitoring', 'Staff training', 'Customer communication', 'Intercom', 'Slack'],
  webSkills: ['React', 'JavaScript', 'Node.js'],
  screenshots: { width: 1200, height: 800 },
  architecture: { width: 1000, height: 600 },
};
