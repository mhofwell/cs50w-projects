import ReactDOM from 'react-dom';

class App extends React.Component {
        render() {
                return (
                        <div>
                                <h1>Welcome!</h1>
                                Hello!
                        </div>
                );
        }
}

ReactDOM.render(<App />, document.querySelector('#app'));
