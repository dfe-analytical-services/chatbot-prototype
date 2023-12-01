import nextJest from 'next/jest.js';

const createJestConfig = nextJest({
  dir: './',
});

/** @type {import('jest').Config} */
const config = {
  collectCoverageFrom: ['src/**/*.{js,jsx,ts,tsx}', '!src/**/*.d.ts'],
  setupFilesAfterEnv: ['<rootDir>/setupTests.js'],
  verbose: true,
  testEnvironment: 'jest-environment-jsdom',
  resetMocks: true,
};

export default createJestConfig(config);
