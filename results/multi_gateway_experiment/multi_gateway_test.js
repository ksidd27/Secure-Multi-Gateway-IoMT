import http from 'k6/http';
import { check } from 'k6';

export const options = {
    scenarios: {
        multi_gateway_test: {
            executor: 'constant-arrival-rate',
            rate: Number(__ENV.RATE || 100),
            timeUnit: '1s',
            duration: __ENV.DURATION || '30s',
            preAllocatedVUs: 15,
            maxVUs: 40,
        },
    },
    thresholds: {
        http_req_failed: ['rate<0.01'],
        http_req_duration: ['p(95)<2000'],
    },
};

const BASE_URL = __ENV.BASE_URL;
const TOKEN = __ENV.JWT_TOKEN || '';

if (!BASE_URL) {
    throw new Error('BASE_URL environment variable is required');
}

export default function () {
    const headers = TOKEN
        ? { Authorization: `Bearer ${TOKEN}` }
        : {};

    const response = http.get(BASE_URL, { headers });

    check(response, {
        'status is 200': (r) => r.status === 200,
        'response contains pong': (r) => r.body.includes('pong'),
    });
}