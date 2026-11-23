import http from 'k6/http';
import { check } from 'k6';

export const options = {
    scenarios: {
        capacity_test: {
            executor: 'constant-arrival-rate',
            rate: 1000,
            timeUnit: '1s',
            duration: '30s',
            preAllocatedVUs: 15,
            maxVUs: 40,
        },
    },
    thresholds: {
        http_req_failed: ['rate<0.01'],
        http_req_duration: ['p(95)<2000'],
    },
};

const BASE_URL = 'http://localhost:8000/edgex-data/api/v1/ping';
const TOKEN = __ENV.JWT_TOKEN;

export default function () {
    const response = http.get(BASE_URL, {
        headers: {
            Authorization: `Bearer ${TOKEN}`,
        },
    });

    check(response, {
        'status is 200': (r) => r.status === 200,
        'response contains pong': (r) => r.body.includes('pong'),
    });
}
