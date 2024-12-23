import requests


class Pamela:
    def __init__(self):
        pass

    def receive_data(
        self,
        address,
        session=None,
        json=True,
        username=None,
        password=None,
        parameters=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
    ):
        """
        Send a GET request and return the response data in the specified format.

        Parameters
        ----------
        address : str
            The address of the API.
        session : requests.Session, optional
            A requests session object to use for sending the request.
        json : bool, optional
            Whether to return the response data as json format. Default is True.
        username : str, optional
            The username to use for basic HTTP authentication.
        password : str, optional
            The password to use for basic HTTP authentication.
        parameters : dict, optional
            The URL parameters to send with the request.
        data : dict, optional
            The data to send in the body of the request.
        headers : dict, optional
            The headers to send with the request.
        cookies : dict, optional
            The cookies to send with the request.
        files : dict, optional
            The files to send with the request.
        timeout : float, optional
            The timeout for the request in seconds. Default is 5 seconds.
        allow_redirects : bool, optional
            Whether to allow redirects. Default is True.
        proxies : dict, optional
            The proxies to use for the request.
        hooks : dict, optional
            The hooks to use for the request.
        stream : bool, optional
            Whether to stream the response content. Default is False.
        verify : bool, optional
            Whether to verify the SSL certificate. Default is True.
        cert : tuple, optional
            The SSL certificate to use for the request.

        Returns
        -------
        data : dict or str
            The response data in the specified format.
        """

        if session:
            response = session.get(
                address,
                params=parameters,
                headers=headers,
                cookies=cookies,
                files=files,
                timeout=timeout,
                allow_redirects=allow_redirects,
                proxies=proxies,
                hooks=hooks,
                stream=stream,
                verify=verify,
                cert=cert,
            )

            # Check if the response is successful
            if response.status_code == 200:
                if json:
                    data = response.json()
                else:
                    data = response.text
                return data

        # if the session didn't work, use a regular request
        if username and password:
            auth = requests.auth.HTTPBasicAuth(username, password)
            response = requests.get(
                address,
                auth=auth,
                params=parameters,
                headers=headers,
                cookies=cookies,
                files=files,
                timeout=timeout,
                allow_redirects=allow_redirects,
                proxies=proxies,
                hooks=hooks,
                stream=stream,
                verify=verify,
                cert=cert,
            )
        else:
            response = requests.get(
                address,
                params=parameters,
                headers=headers,
                cookies=cookies,
                files=files,
                timeout=timeout,
                allow_redirects=allow_redirects,
                proxies=proxies,
                hooks=hooks,
                stream=stream,
                verify=verify,
                cert=cert,
            )

        # Check if the response is successful
        if response.status_code == 200:
            if json:
                data = response.json()
            else:
                data = response.text
            return data
        else:
            return None

    def send_data(
        self,
        address,
        data=None,
        session=None,
        username=None,
        password=None,
        parameters=None,
        headers=None,
        cookies=None,
        files=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
    ):
        if session:
            response = session.post(
                address,
                data=data,
                params=parameters,
                headers=headers,
                cookies=cookies,
                files=files,
                timeout=timeout,
                allow_redirects=allow_redirects,
                proxies=proxies,
                hooks=hooks,
                stream=stream,
                verify=verify,
                cert=cert,
            )
            return response

        # if the session didn't work, use a regular request
        if username and password:
            auth = requests.auth.HTTPBasicAuth(username, password)
            response = requests.post(
                address,
                data=data,
                auth=auth,
                params=parameters,
                headers=headers,
                cookies=cookies,
                files=files,
                timeout=timeout,
                allow_redirects=allow_redirects,
                proxies=proxies,
                hooks=hooks,
                stream=stream,
                verify=verify,
                cert=cert,
            )
        else:
            response = requests.post(
                address,
                data=data,
                params=parameters,
                headers=headers,
                cookies=cookies,
                files=files,
                timeout=timeout,
                allow_redirects=allow_redirects,
                proxies=proxies,
                hooks=hooks,
                stream=stream,
                verify=verify,
                cert=cert,
            )

        return response


class Session:
    def __init__(self):
        pass

    def create(address, username, password):
        """
        Create a requests session for a given address and credentials.

        Parameters
        ----------
        address : str
            The address to which the session will connect.
        username : str
            The username to use for authentication.
        password : str
            The password to use for authentication.

        Returns
        -------
        session : requests.Session
            The session created by the function.
        """

        session = requests.Session()
        session.auth = (username, password)
        session.post(address)
        return session

    def status(address, session):
        """
        Get the status code of a POST request to a given address
        using a given session.

        Parameters
        ----------
        address : str
            The address to which the request is sent.
        session : requests.Session
            The session to use for sending the request.

        Returns
        -------
        status_code : int
            The HTTP status code of the response.
        """

        response = session.post(address)
        return response.status_code
