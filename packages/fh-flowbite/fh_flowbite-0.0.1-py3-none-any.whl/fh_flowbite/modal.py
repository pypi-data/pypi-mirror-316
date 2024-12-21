from .flowbite import Flowbite, extends
import fh_tailwind.modal as fh_tailwind

class Modal(Flowbite, fh_tailwind.Modal):
    
    @extends(fh_tailwind.Modal)
    @staticmethod
    def show_script(id: str, placement: str = "center", backdrop: str = "static", closable: bool = False, on_show: str = None, on_hide: str = None, on_toggle: str = None):
        """Generates a FlowBite JavaScript script to show a modal with the specified options.

        Args:
            id (str): The ID of the modal element.
            placement (str, optional): Set the position of the modal element relative to the document body. 
                Choose one of the values from {top|center|right}-{left|center|right}. 
                Defaults to "center".
            backdrop (str, optional): Choose between "static" or "dynamic" to prevent closing the modal when clicking outside. 
                Defaults to "static".
            closable (bool, optional): Set to False to disable closing the modal on hitting ESC or clicking on the backdrop. 
                Defaults to False.
            on_show (str, optional): JavaScript code to set a callback function when the modal has been shown. 
                Defaults to None.
            on_hide (str, optional): JavaScript code to set a callback function when the modal has been hidden. 
                Defaults to None.
            on_toggle (str, optional): JavaScript code to set a callback function when the modal visibility has been toggled. 
                Defaults to None.
        Returns:
            str: A JavaScript script to show the modal with the specified options.
        """

        return f"""
        const options = {{
            placement: '{placement}',
            backdrop: '{backdrop}',
            closable: {'true' if closable else 'false'},
            onShow: () => {{                
                {on_show or ''}
            }},
            onHide: () => {{     
                {on_hide or ''}         
            }},            
            onToggle: () => {{           
                {on_toggle or ''}     
            }},
        }};

        const modal = new Modal(document.getElementById('{id}'), options);
        modal.show();
        """
    
    @extends(fh_tailwind.Modal)
    @staticmethod
    def hide_script(id: str):
        """Generates a FlowBite JavaScript script to hide a modal with the specified ID.
        
        Args:
            id (str): The ID of the modal element.
        """

        return f"""
        const modal = new Modal(document.getElementById('{id}'));
        modal.hide();
        """
    
    @extends(fh_tailwind.Modal)
    @staticmethod
    def toggle_script(id: str):
        """Generates a FlowBite JavaScript script to toggle the visibility of a modal with the specified ID.

        Args:
            id (str): The ID of the modal element.
        """

        return f"""
        const modal = new Modal(document.getElementById('{id}'));
        modal.toggle();
        """
