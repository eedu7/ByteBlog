import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

import SignInForm from "./SignInForm";

const SignInCard = () => {
    return (
        <Card className="w-[450px]">
            <CardHeader>
                <CardTitle>Ready to Continue?</CardTitle>
                <CardDescription>
                    Log in now to continue reading your favorite articles,
                    comment on discussions, and enjoy new content&rsquo;
                </CardDescription>
            </CardHeader>
            <CardContent>
                <SignInForm />
            </CardContent>
            <CardFooter>
                <h1 className="text-center">Social Authentication</h1>
            </CardFooter>
        </Card>
    );
};

export default SignInCard;
