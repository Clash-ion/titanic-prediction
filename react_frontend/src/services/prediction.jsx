import axios from 'axios';
import process from 'process';

const apiUrl = process.env.FLASK_APP_API_URL ?? 'http://localhost:3000';

const predictSurvival = async (query) => {
	return await axios.get(apiUrl, {
		params: query
	});
};

export default predictSurvival;