import { validate } from '../validate-cards.mjs';
import assert from 'node:assert';

const passRes = await validate('test/fixtures/pass.html');
assert.equal(passRes.ok, true, 'pass.html 应通过: ' + JSON.stringify(passRes.failures));

const overflowRes = await validate('test/fixtures/overflow.html');
assert.equal(overflowRes.ok, false, 'overflow.html 应失败');
assert.ok(overflowRes.failures.some(f => f.rule === 'R1'), '应含 R1 失败');

console.log('ALL TESTS PASSED');
