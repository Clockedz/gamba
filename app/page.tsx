"use client";
import Win from "@/components/win";
import Neutral from "@/components/neutral";
import Lose from "@/components/lose";
import React from "react";
import Image from "next/image";
import Link from "next/link";

export default function Home() {
	const [player, setPlayer] = React.useState("");

	const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setPlayer(event.target.value);
	};
	return (
		<main className="flex h-screen w-screen flex-col items-center justify-evenly bg-[#171a21]">
			<div className="w-full h-12 flex justify-center">
				<input
					className="w-1/3 bg-white text-black rounded-lg"
					type="text"
					value={player}
					placeholder="Enter player name..."
					onChange={handleInputChange}
				/>
			</div>

			<div className="flex flex-row justify-around w-full h-1/2">
				<Win player={player} />
				<Neutral player={player} />
				<Lose player={player} />
			</div>
			<div></div>
			<footer className="absolute bottom-0 pb-5 flex items-center justify-evenly">
				<Link
					href="https://www.youtube.com/channel/UCVDhsF3laZ1cZPSc_FmHEtQ"
					target="_blank"
				>
					<Image
						src="/youtube.png"
						width={30}
						height={30}
						alt="Picture of the author"
					/>
				</Link>

				<p className="pl-1">Developed by @clockxyz</p>
			</footer>
		</main>
	);
}
