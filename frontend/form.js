const form = document.getElementById('patient-form');
const fields = ['name', 'age', 'email'];

const schema = yup.object({
  name: yup.string().required('Name is required'),
  age: yup.number().typeError('Age must be a number').required('Age is required'),
  email: yup.string().email('Invalid email').required('Email is required'),
});

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearErrors();
  const data = {
    name: form.name.value.trim(),
    age: form.age.value,
    email: form.email.value.trim(),
  };
  try {
    await schema.validate(data, { abortEarly: false });
    const response = await fetch('/generate-note', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      const message = await response.text();
      throw new Error(message || 'Request failed');
    }
    document.getElementById('serverError').textContent = 'Note generated successfully';
  } catch (err) {
    if (err.name === 'ValidationError') {
      err.inner.forEach(({ path, message }) => {
        const input = document.getElementById(path);
        input.classList.add('error');
        document.getElementById(`${path}Error`).textContent = message;
      });
    } else {
      document.getElementById('serverError').textContent = `Error: ${err.message}`;
    }
  }
});

function clearErrors() {
  fields.forEach((field) => {
    const input = document.getElementById(field);
    input.classList.remove('error');
    document.getElementById(`${field}Error`).textContent = '';
  });
  document.getElementById('serverError').textContent = '';
}
