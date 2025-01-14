import config from '../config.json';  // Import the config file
const SERVER_URL = `${config.backend.url}`;

export default async function requestUserAuthRegister(email, password, firstName, lastName) {
    const data = {
        email: email,
        password: password,  
        firstName: firstName,
        lastName: lastName
    };

    try { 
        console.log("0"); // FIXME: Error in here.
        const response = await fetch(SERVER_URL + '/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow_Origin': '*'
            },
            body: JSON.stringify(data),
            credentials: 'include' // Include cookies
        });
        // FIXME: yo
        console.log("1");
   
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Unknown error occurred');
        }

        const result = await response.json(); // Parse JSON response
        console.log('Response from server:', result);
        return result.csrf_token; 
    } catch (error) {
        console.error('Error during registration:', error);
        throw error; // Re-throw the error so it can be handled in handleSubmit
    }
}
