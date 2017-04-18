var React = require('react');
var ReactRouter = require('react-router-dom');
var Router = ReactRouter.BrowserRouter;
var Route = ReactRouter.Route;
var Link = ReactRouter.Link;
var Main = require('../components/Main');
var Home = require('../components/Home');
import { Data } from '../components/Home';

var routes = (
    <Router>
        <div>
            <ul>
                <li><Link to='/'>Main</Link></li>
                <li><Link to='/home'>Home</Link></li>
            </ul>
            <hr/>
            <Route exact path='/' component={Main} />
            <Route path='/home' component={Home} />
            <Route path='/data' component={Data} />
        </div>
    </Router>
);

export { routes} ;