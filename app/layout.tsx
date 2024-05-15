import './globals.css'
import {Noto_Sans} from "next/font/google";

const noto = Noto_Sans({
	weight: ["100", "200", "400", "600"],
	subsets: ["latin"],
});

export const metadata = {
	title: "gamba",
	description: "Created by @Clockxyz on YT",
};

export default function RootLayout({children}: {children: React.ReactNode}) {
	return (
		<html lang="en">
			<body className={noto.className}>{children}</body>
		</html>
	);
}
