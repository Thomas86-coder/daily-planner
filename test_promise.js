const p1 = Promise.resolve({ data: 'todosData' });
const p2 = Promise.resolve({ data: { content: 'hello' } }); // like maybeSingle() returning a row
const p3 = Promise.resolve({ data: null }); // maybeSingle() with no rows

async function test() {
  const [{ data: td1 }, { data: review1 }] = await Promise.all([p1, p2]);
  console.log("Review 1:", review1); // Expect: { content: 'hello' }

  const [{ data: td2 }, { data: review2 }] = await Promise.all([p1, p3]);
  console.log("Review 2:", review2); // Expect: null
}
test();
