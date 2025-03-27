import React, { useContext } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";
import { SummaryForm } from "../component/SummaryForm.jsx";

export const Home = () => {
	const { store, actions } = useContext(Context);

	return (
		<div className="text-center mt-5">
			<div className="container bg-dark text-white p-3">


			<h1 className="p-2">Bienvenido a la app de resumen</h1>
			<SummaryForm />
			</div>
		</div>
	);
};
