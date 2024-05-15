"use client";
import React, {useState, useEffect} from "react";

export default function Lose({player}) {
	const [data, setData] = useState(null);

	useEffect(() => {
		const fetchData = async () => {
			try {
				const response = await fetch(
					`/api/lose?player=${encodeURIComponent(player)}`
				);
				if (!response.ok) {
					throw new Error("Network response was not ok");
				}
				const responseData = await response.json();
				setData(responseData);
			} catch (error) {
				console.error("Error fetching data:", error);
			}
		};

		fetchData();
	}, [player]);

	return (
		<div className="w-1/4 h-36 border-[#ff0000] border-4 rounded-md flex flex-col">
			<div className="bg-[#ff0000] flex text-black w-full h-full justify-center items-center ">
				<h2 className="">Lose</h2>
			</div>

			{data && (
				<div className="bg-black flex justify-center items-center flex-col">
					<p>fantasy points: {data.fpoints}</p>
					<p>kills: {data.kills}</p>
					<p>deaths: {data.deaths}</p>
					<p>assists: {data.assists}</p>
				</div>
			)}
		</div>
	);
}
