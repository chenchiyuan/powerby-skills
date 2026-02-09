module.exports = {
  testEnvironment: 'node',
  testMatch: [
    '**/tests/**/*.test.js'
  ],
  collectCoverageFrom: [
    'src/**/*.js',
    '!src/hooks/*.js',
    '!src/index.js'
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov'],
  coverageThreshold: {
    global: {
      branches: 25,
      functions: 25,
      lines: 25,
      statements: 25
    }
  },
  verbose: true,
  testTimeout: 10000
};
