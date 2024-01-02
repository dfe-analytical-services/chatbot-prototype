import nextJest from 'next/jest.js';

process.env.NODE_ENV = 'test';

const createJestConfig = nextJest({
  dir: './',
});

/** @type {import('jest').Config} */
const config = {
  collectCoverageFrom: ['./**/*.{ts,tsx}', '!./**/*.d.ts'],
  setupFilesAfterEnv: ['<rootDir>/setupTests.js'],
  verbose: true,
  testEnvironment: 'jest-environment-jsdom',
  resetMocks: true,
  reporters: ['default', 'jest-junit'],
  moduleNameMapper: {
    '^.+\\.(svg)$': '<rootDir>/__mocks__/svg.js',
  },
};

export default createJestConfig(config);
