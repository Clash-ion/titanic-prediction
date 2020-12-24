import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_URL ?? 'http://localhost:3000';

const predictSurvival = async (query) => {
	return await axios.get(apiUrl, {
		params: query
	});
};

export default predictSurvival;